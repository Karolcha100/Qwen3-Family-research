import argparse
import json
from pathlib import Path

import torch
from torch import nn
from transformers import AutoModelForCausalLM, AutoTokenizer, PreTrainedModel

from qwen_compression.model_parts import decoder_layers
from qwen_compression.progress import report_progress

MODEL_NAME = "Qwen/Qwen3-0.6B-Base"
ORIGINAL = "original"
REDUCED_PRECISION = "original-bf16"
DATASETS = ("humaneval", "mbpp")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mlps", type=Path, default=Path("/home/karol/qwen3-checkpoints/phase2-code/mlps"))
    parser.add_argument(
        "--evaluation-set", type=Path, default=Path("/home/karol/qwen3-checkpoints/phase2-code/evaluation-set.pt")
    )
    parser.add_argument("--code-evaluation", type=Path, default=Path("results/phase2/code-eval"))
    parser.add_argument("--problems-directory", type=Path, default=Path("results/phase2/code-eval"))
    parser.add_argument("--output", type=Path, default=Path("results/phase2/code-eval/token-agreement.json"))
    return parser.parse_args()


def load_model(dtype: torch.dtype) -> PreTrainedModel:
    torch.backends.cuda.matmul.allow_tf32 = False
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, dtype=dtype, device_map="cuda").eval()
    model.requires_grad_(False)
    return model


def load_variants(directory: Path) -> dict[str, tuple[int, nn.Module]]:
    variants = {}
    for path in sorted(directory.glob("*.pt")):
        stored = torch.load(path, weights_only=False)
        variants[path.stem] = (stored["layer"], stored["mlp"].to(device="cuda", dtype=torch.float32))
    return variants


@torch.no_grad()
def variant_log_probabilities(
    model: PreTrainedModel, token_ids: torch.Tensor, layer_index: int, mlp: nn.Module
) -> torch.Tensor:
    layer = decoder_layers(model)[layer_index]
    original_mlp = layer.mlp
    layer.mlp = mlp
    try:
        return torch.log_softmax(model(token_ids.unsqueeze(0)).logits[0].float(), dim=-1)
    finally:
        layer.mlp = original_mlp


def agreement_statistics(
    reference: torch.Tensor, reference_tokens: torch.Tensor, log_probabilities: torch.Tensor
) -> dict[str, float]:
    return {
        "kl_sum": (reference.exp() * (reference - log_probabilities)).sum().item(),
        "agreeing": (log_probabilities.argmax(dim=-1) == reference_tokens).sum().item(),
        "tokens": reference_tokens.numel(),
    }


@torch.no_grad()
def compare_sequence(
    model: PreTrainedModel,
    reduced_precision_model: PreTrainedModel,
    variants: dict[str, tuple[int, nn.Module]],
    token_ids: torch.Tensor,
    positions: slice,
) -> dict[str, dict[str, float]]:
    reference = torch.log_softmax(model(token_ids.unsqueeze(0)).logits[0].float(), dim=-1)[positions]
    reference_tokens = reference.argmax(dim=-1)
    reduced_precision = torch.log_softmax(reduced_precision_model(token_ids.unsqueeze(0)).logits[0].float(), dim=-1)[
        positions
    ]
    statistics = {REDUCED_PRECISION: agreement_statistics(reference, reference_tokens, reduced_precision)}
    del reduced_precision
    for name, (layer_index, mlp) in variants.items():
        statistics[name] = agreement_statistics(
            reference,
            reference_tokens,
            variant_log_probabilities(model, token_ids, layer_index, mlp)[positions],
        )
    return statistics


def solved_tasks(summary: dict) -> set[str]:
    return {
        task_id
        for task_id, task in summary["per_task"].items()
        if task["base_status"] == "pass" and task["plus_status"] == "pass"
    }


def main() -> None:
    arguments = parse_arguments()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = load_model(torch.float32)
    reduced_precision_model = load_model(torch.bfloat16)
    variants = load_variants(arguments.mlps)
    evaluation = torch.load(arguments.evaluation_set)
    problems = {
        dataset: {
            problem["task_id"]: problem["prompt"].strip() + "\n"
            for problem in map(
                json.loads, (arguments.problems_directory / f"{dataset}-problems.jsonl").read_text().splitlines()
            )
        }
        for dataset in DATASETS
    }
    original_solutions = {
        dataset: {
            row["task_id"]: row["solution"]
            for row in map(
                json.loads, (arguments.code_evaluation / ORIGINAL / f"{dataset}.jsonl").read_text().splitlines()
            )
        }
        for dataset in DATASETS
    }
    total_work = evaluation["token_ids"].shape[0] + sum(len(solutions) for solutions in original_solutions.values())
    finished_work = 0
    totals: dict[str, dict[str, dict[str, float]]] = {}
    for token_ids, source in zip(evaluation["token_ids"], evaluation["sources"], strict=True):
        for name, values in compare_sequence(
            model, reduced_precision_model, variants, token_ids.to("cuda"), slice(None)
        ).items():
            accumulated = totals.setdefault(source, {}).setdefault(name, {"kl_sum": 0.0, "agreeing": 0, "tokens": 0})
            for key, value in values.items():
                accumulated[key] += value
        finished_work += 1
        report_progress(finished_work / total_work)
    unchanged_answers: dict[str, dict[str, list[str]]] = {}
    for dataset in DATASETS:
        for task_id, solution in original_solutions[dataset].items():
            prompt_ids = tokenizer(problems[dataset][task_id], return_tensors="pt").input_ids[0]
            completion_ids = tokenizer(
                solution.removeprefix(problems[dataset][task_id]), return_tensors="pt"
            ).input_ids[0]
            if completion_ids.numel() == 0:
                finished_work += 1
                continue
            token_ids = torch.cat([prompt_ids, completion_ids]).to("cuda")
            positions = slice(prompt_ids.numel() - 1, token_ids.numel() - 1)
            for name, values in compare_sequence(
                model, reduced_precision_model, variants, token_ids, positions
            ).items():
                accumulated = totals.setdefault(dataset, {}).setdefault(
                    name, {"kl_sum": 0.0, "agreeing": 0, "tokens": 0}
                )
                for key, value in values.items():
                    accumulated[key] += value
                if values["agreeing"] == values["tokens"]:
                    unchanged_answers.setdefault(dataset, {}).setdefault(name, []).append(task_id)
            finished_work += 1
            report_progress(finished_work / total_work)
    summary: dict[str, dict] = {"sets": {}, "evalplus": {}}
    for source, by_name in totals.items():
        summary["sets"][source] = {
            name: {
                "kl": values["kl_sum"] / values["tokens"],
                "top1_agreement": values["agreeing"] / values["tokens"],
                "tokens": values["tokens"],
            }
            for name, values in by_name.items()
        }
    for dataset in DATASETS:
        original_solved = solved_tasks(
            json.loads((arguments.code_evaluation / ORIGINAL / f"{dataset}-summary.json").read_text())
        )
        for directory in sorted(arguments.code_evaluation.iterdir()):
            efficiency_path = directory / f"{dataset}-efficiency.json"
            summary_path = directory / f"{dataset}-summary.json"
            if directory.name == ORIGINAL or not efficiency_path.exists() or not summary_path.exists():
                continue
            mlp_paths = json.loads(efficiency_path.read_text())["mlps"]
            if len(mlp_paths) != 1:
                continue
            name = Path(mlp_paths[0]).stem
            unchanged = set(unchanged_answers.get(dataset, {}).get(name, []))
            changed_result = solved_tasks(json.loads(summary_path.read_text())) ^ original_solved
            summary["evalplus"].setdefault(dataset, {})[directory.name] = {
                "variant": name,
                "tasks": len(original_solutions[dataset]),
                "unchanged_answers": len(unchanged),
                "changed_results": len(changed_result),
                "changed_results_with_unchanged_answer": len(changed_result & unchanged),
            }
        summary["evalplus"].setdefault(dataset, {})[REDUCED_PRECISION] = {
            "variant": REDUCED_PRECISION,
            "tasks": len(original_solutions[dataset]),
            "unchanged_answers": len(unchanged_answers.get(dataset, {}).get(REDUCED_PRECISION, [])),
        }
    arguments.output.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
