import argparse
import json
import time
from pathlib import Path
from typing import Any, cast

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Qwen3ForCausalLM

from qwen_compression.model_parts import decoder_layers
from qwen_compression.progress import report_progress

MODEL_NAME = "Qwen/Qwen3-0.6B-Base"
COMMON_STOP_TEXTS = ["<|endoftext|>", "<|endofmask|>", "</s>", "\nif __name__", "\ndef main(", "\nprint("]
DATASET_STOP_TEXTS = {
    "humaneval": ["\ndef ", "\nclass ", "\nimport ", "\nfrom ", "\nassert "],
    "mbpp": ['\n"""', "\nassert"],
}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=["humaneval", "mbpp"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--problems-directory", type=Path, default=Path("results/phase2/code-eval"))
    parser.add_argument("--mlps", type=Path, nargs="*", default=[])
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--max-new-tokens", type=int, default=768)
    parser.add_argument("--samples-per-task", type=int, default=1)
    parser.add_argument("--temperature", type=float, default=0.8)
    parser.add_argument("--top-p", type=float, default=0.95)
    parser.add_argument("--seed", type=int, default=1)
    return parser.parse_args()


def load_model(mlp_paths: list[Path]) -> Qwen3ForCausalLM:
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, dtype=torch.bfloat16, device_map="cuda").eval()
    for mlp_path in mlp_paths:
        stored = torch.load(mlp_path, weights_only=False)
        decoder_layers(model)[stored["layer"]].mlp = stored["mlp"].to(device=model.device, dtype=torch.bfloat16)
    model.requires_grad_(False)
    assert isinstance(model, Qwen3ForCausalLM)
    return model


def truncated(completion: str, stop_texts: list[str]) -> str:
    end = min([completion.index(text) for text in stop_texts if text in completion], default=len(completion))
    return completion[:end].replace("\t", "    ")


@torch.inference_mode()
def main() -> None:
    arguments = parse_arguments()
    problems = [
        json.loads(line)
        for line in (arguments.problems_directory / f"{arguments.dataset}-problems.jsonl").read_text().splitlines()
    ]
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, padding_side="left")
    model = load_model(arguments.mlps)
    stop_texts = COMMON_STOP_TEXTS + DATASET_STOP_TEXTS[arguments.dataset]
    prompts = {problem["task_id"]: problem["prompt"].strip() + "\n" for problem in problems}
    order = sorted(prompts, key=lambda task_id: len(prompts[task_id]))
    solutions: dict[str, list[str]] = {}
    sampling = arguments.samples_per_task > 1
    prompts_per_batch = max(1, arguments.batch_size // arguments.samples_per_task)
    torch.manual_seed(arguments.seed)
    generated_tokens = 0
    torch.cuda.reset_peak_memory_stats()
    start = time.perf_counter()
    for batch_start in range(0, len(order), prompts_per_batch):
        task_ids = order[batch_start : batch_start + prompts_per_batch]
        encoded = tokenizer([prompts[task_id] for task_id in task_ids], return_tensors="pt", padding=True).to(
            model.device
        )
        outputs = cast(Any, model).generate(
            **encoded,
            max_new_tokens=arguments.max_new_tokens,
            do_sample=sampling,
            num_return_sequences=arguments.samples_per_task,
            **({"temperature": arguments.temperature, "top_p": arguments.top_p} if sampling else {}),
            stop_strings=stop_texts,
            tokenizer=tokenizer,
            pad_token_id=tokenizer.pad_token_id,
        )
        new_tokens = outputs[:, encoded.input_ids.shape[1] :]
        generated_tokens += int((new_tokens != tokenizer.pad_token_id).sum().item())
        completions = tokenizer.batch_decode(new_tokens, skip_special_tokens=True)
        for position, task_id in enumerate(task_ids):
            solutions[task_id] = [
                prompts[task_id] + truncated(completion, stop_texts)
                for completion in completions[
                    position * arguments.samples_per_task : (position + 1) * arguments.samples_per_task
                ]
            ]
        report_progress(len(solutions) / len(order))
    seconds = time.perf_counter() - start
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        "".join(
            json.dumps({"task_id": task_id, "solution": solution}) + "\n"
            for task_id in prompts
            for solution in solutions[task_id]
        )
    )
    efficiency = {
        "dataset": arguments.dataset,
        "mlps": [str(path) for path in arguments.mlps],
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
        "peak_memory_bytes": torch.cuda.max_memory_allocated(),
        "generated_tokens": generated_tokens,
        "seconds": seconds,
        "tokens_per_second": generated_tokens / seconds,
        "batch_size": arguments.batch_size,
        "samples_per_task": arguments.samples_per_task,
        "temperature": arguments.temperature if sampling else 0.0,
        "top_p": arguments.top_p if sampling else 1.0,
    }
    arguments.output.with_name(arguments.output.name.replace(".jsonl", "-efficiency.json")).write_text(
        json.dumps(efficiency, indent=2)
    )
    print(json.dumps(efficiency, indent=2))


if __name__ == "__main__":
    main()
