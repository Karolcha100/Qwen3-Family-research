import argparse
import copy
import json
import math
import time
from pathlib import Path

import torch
from datasets import load_dataset
from torch import nn
from transformers import AutoModelForCausalLM, AutoTokenizer, PreTrainedModel

from qwen_compression.data import load_or_build_measurement_set
from qwen_compression.metrics import kl_and_loss_change, reference_log_probabilities
from qwen_compression.model_parts import (
    decoder_layers,
    down_projection,
    final_hidden_states,
    hidden_states_before_layer,
    mlp_of,
    replaced_mlp,
    run_layer_window,
)
from qwen_compression.reconstruction import LeastSquaresStatistics, pruned_mlp

MODEL_NAME = "Qwen/Qwen3-0.6B-Base"
SHARD_SEQUENCES = 32


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--layer", type=int, required=True)
    parser.add_argument("--removed-fractions", type=float, nargs="+", default=[0.05, 0.10, 0.20, 0.40])
    parser.add_argument("--importances", nargs="+", default=["perturbation", "activation"])
    parser.add_argument("--training-sequences", type=int, default=488)
    parser.add_argument("--sequence-length", type=int, default=2048)
    parser.add_argument("--measurement-sequences", type=int, nargs="+", default=[0, 3])
    parser.add_argument("--epochs", type=int, default=4)
    parser.add_argument("--learning-rate", type=float, default=5e-5)
    parser.add_argument("--batch-sequences", type=int, default=4)
    parser.add_argument("--relative-ridge", type=float, default=1e-6)
    parser.add_argument("--chunk-length", type=int, default=256)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--data-directory", type=Path, default=Path.home() / "qwen3-checkpoints/phase2")
    parser.add_argument("--stage1", type=Path, default=Path("results/phase2/stage1"))
    parser.add_argument("--stage2", type=Path, default=Path("results/phase2/stage2"))
    parser.add_argument("--output", type=Path, default=Path("results/phase2/stage4"))
    parser.add_argument("--previous-map", type=Path, default=Path("results/phase2/stage2/fisher-map.pt"))
    parser.add_argument("--evaluation-set", type=Path, default=None)
    return parser.parse_args()


def log_event(output: Path, record: dict[str, object]) -> None:
    record = {"time": time.strftime("%Y-%m-%d %H:%M:%S"), **record}
    with (output / "log.jsonl").open("a") as log_file:
        log_file.write(json.dumps(record) + "\n")
    print(json.dumps(record), flush=True)


def load_model() -> PreTrainedModel:
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, dtype=torch.float32, device_map="cuda").eval()
    model.requires_grad_(False)
    return model


@torch.no_grad()
def collect_pairs(
    model: PreTrainedModel, token_ids: torch.Tensor, layer_index: int, pair_directory: Path
) -> LeastSquaresStatistics:
    statistics_path = pair_directory / "least-squares.pt"
    if statistics_path.exists():
        return torch.load(statistics_path, weights_only=False)
    pair_directory.mkdir(parents=True, exist_ok=True)
    width, hidden_size = model.config.intermediate_size, model.config.hidden_size
    statistics = LeastSquaresStatistics(width, hidden_size)

    def record(module: nn.Module, arguments: tuple[torch.Tensor, ...], output: torch.Tensor) -> None:
        statistics.add(arguments[0], output)

    handle = down_projection(model, layer_index).register_forward_hook(record)
    try:
        for shard_index, start in enumerate(range(0, token_ids.shape[0], SHARD_SEQUENCES)):
            inputs, targets = [], []
            for sequence in token_ids[start : start + SHARD_SEQUENCES]:
                hidden = model.model(
                    input_ids=sequence.unsqueeze(0).to(model.device), output_hidden_states=True, use_cache=False
                ).hidden_states
                inputs.append(hidden[layer_index].bfloat16().cpu())
                targets.append(hidden[layer_index + 2].bfloat16().cpu())
            torch.save(
                {"inputs": torch.cat(inputs), "targets": torch.cat(targets)},
                pair_directory / f"shard-{shard_index:03d}.pt",
            )
    finally:
        handle.remove()
    torch.save(statistics, statistics_path)
    return statistics


def neuron_importance(kind: str, layer_index: int, arguments: argparse.Namespace) -> torch.Tensor:
    if kind == "activation":
        return torch.load(arguments.stage1 / "statistics.pt")["mean_absolute"][layer_index].float()
    if kind == "previous-map":
        return torch.load(arguments.previous_map)["coefficients"][layer_index].float()
    return torch.load(arguments.stage2 / "fisher-map.pt")["coefficients"][layer_index].float()


def train_through_next_layer(
    model: PreTrainedModel,
    layer_index: int,
    student_mlp: nn.Module,
    pair_directory: Path,
    arguments: argparse.Namespace,
) -> dict[str, float | int | list[float]]:
    layers = decoder_layers(model)
    student_layer = copy.deepcopy(layers[layer_index])
    student_layer.mlp = student_mlp
    student_mlp.requires_grad_(True)
    optimizer = torch.optim.Adam(student_mlp.parameters(), lr=arguments.learning_rate)
    shards = sorted(pair_directory.glob("shard-*.pt"))
    training_shards, validation_shard = shards[:-1], shards[-1]

    def window_loss(inputs: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        output = run_layer_window(model, inputs.to(model.device).float(), [student_layer, layers[layer_index + 1]])
        target = targets.to(model.device).float()
        return (output - target).square().mean() / target.var()

    def validation_loss() -> float:
        validation = torch.load(validation_shard)
        with torch.no_grad():
            losses = [
                window_loss(
                    validation["inputs"][start : start + arguments.batch_sequences],
                    validation["targets"][start : start + arguments.batch_sequences],
                ).item()
                for start in range(0, validation["inputs"].shape[0], arguments.batch_sequences)
            ]
        return sum(losses) / len(losses)

    before = validation_loss()
    best_loss, best_state, best_epoch = before, copy.deepcopy(student_mlp.state_dict()), 0
    generator = torch.Generator().manual_seed(arguments.seed)
    epoch_losses = []
    for epoch in range(1, arguments.epochs + 1):
        for shard_index in torch.randperm(len(training_shards), generator=generator).tolist():
            shard = torch.load(training_shards[shard_index])
            order = torch.randperm(shard["inputs"].shape[0], generator=generator)
            for start in range(0, order.numel(), arguments.batch_sequences):
                batch = order[start : start + arguments.batch_sequences]
                loss = window_loss(shard["inputs"][batch], shard["targets"][batch])
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
        epoch_loss = validation_loss()
        epoch_losses.append(epoch_loss)
        if epoch_loss < best_loss:
            best_loss, best_state, best_epoch = epoch_loss, copy.deepcopy(student_mlp.state_dict()), epoch
    student_mlp.load_state_dict(best_state)
    student_mlp.requires_grad_(False)
    return {
        "window_loss_before": before,
        "window_loss_after": best_loss,
        "best_epoch": best_epoch,
        "epoch_losses": epoch_losses,
    }


@torch.no_grad()
def kl_to_original(
    model: PreTrainedModel, layer_index: int, mlp: nn.Module, token_ids: torch.Tensor, chunk_length: int
) -> dict[str, float]:
    kl_total, loss_total = 0.0, 0.0
    for sequence in token_ids:
        sequence = sequence.to(model.device)
        embeddings = hidden_states_before_layer(model, sequence.unsqueeze(0), 0)
        reference = reference_log_probabilities(model, final_hidden_states(model, embeddings, 0), chunk_length)
        with replaced_mlp(model, layer_index, mlp):
            perturbed = final_hidden_states(model, embeddings, 0)
        kl, loss_change = kl_and_loss_change(model, perturbed, reference, sequence, chunk_length)
        kl_total += kl.item()
        loss_total += loss_change.item()
    return {"kl": kl_total / token_ids.shape[0], "loss_change": loss_total / token_ids.shape[0]}


@torch.no_grad()
def wikitext2_perplexity(model: PreTrainedModel, wikitext_ids: torch.Tensor, context_length: int) -> float:
    window_count = wikitext_ids.shape[1] // context_length
    negative_log_likelihood = 0.0
    for window_index in range(window_count):
        window = wikitext_ids[:, window_index * context_length : (window_index + 1) * context_length].to(model.device)
        negative_log_likelihood += model(window, labels=window).loss.item() * (context_length - 1)
    return math.exp(negative_log_likelihood / (window_count * (context_length - 1)))


def evaluate(
    model: PreTrainedModel,
    layer_index: int,
    mlp: nn.Module,
    measurement_ids: torch.Tensor,
    wikitext_ids: torch.Tensor,
    arguments: argparse.Namespace,
    evaluation_sets: dict[str, torch.Tensor],
) -> dict[str, float]:
    result = kl_to_original(model, layer_index, mlp, measurement_ids, arguments.chunk_length)
    for source, token_ids in evaluation_sets.items():
        held_out = kl_to_original(model, layer_index, mlp, token_ids, arguments.chunk_length)
        result[f"kl_{source}"], result[f"loss_change_{source}"] = held_out["kl"], held_out["loss_change"]
    with replaced_mlp(model, layer_index, mlp):
        result["wikitext2_perplexity"] = wikitext2_perplexity(model, wikitext_ids, arguments.sequence_length)
    return result


def main() -> None:
    arguments = parse_arguments()
    output = arguments.output / f"layer-{arguments.layer:02d}"
    output.mkdir(parents=True, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    training_ids, _ = load_or_build_measurement_set(
        arguments.data_directory / "training-set.pt",
        tokenizer,
        arguments.training_sequences,
        arguments.sequence_length,
        3,
        arguments.seed,
    )
    measurement_ids = torch.load(arguments.data_directory / "measurement-set.pt")["token_ids"][
        arguments.measurement_sequences
    ]
    evaluation_sets: dict[str, torch.Tensor] = {}
    if arguments.evaluation_set is not None:
        evaluation = torch.load(arguments.evaluation_set)
        for source in sorted(set(evaluation["sources"])):
            rows = [index for index, name in enumerate(evaluation["sources"]) if name == source]
            evaluation_sets[source] = evaluation["token_ids"][rows]
    wikitext_text = "\n\n".join(load_dataset("Salesforce/wikitext", "wikitext-2-raw-v1", split="test")["text"])
    wikitext_ids = tokenizer(wikitext_text, return_tensors="pt").input_ids
    log_event(output, {"step": "start", "arguments": {key: str(value) for key, value in vars(arguments).items()}})
    model = load_model()
    results_path = output / "results.jsonl"
    done = set()
    if results_path.exists():
        done = {
            (row["importance"], row["removed_fraction"], row["variant"])
            for row in map(json.loads, results_path.read_text().splitlines())
        }
    if ("original", 0.0, "original") not in done:
        original_perplexity = wikitext2_perplexity(model, wikitext_ids, arguments.sequence_length)
        with results_path.open("a") as results_file:
            results_file.write(
                json.dumps(
                    {
                        "importance": "original",
                        "removed_fraction": 0.0,
                        "variant": "original",
                        "kl": 0.0,
                        "loss_change": 0.0,
                        "wikitext2_perplexity": original_perplexity,
                    }
                )
                + "\n"
            )
    start = time.perf_counter()
    statistics = collect_pairs(
        model, training_ids, arguments.layer, arguments.data_directory / f"layer-{arguments.layer:02d}-pairs"
    )
    log_event(output, {"step": "pairs", "tokens": statistics.token_count, "seconds": time.perf_counter() - start})
    original_mlp = mlp_of(model, arguments.layer)
    width = model.config.intermediate_size
    for importance_kind in arguments.importances:
        importance = neuron_importance(importance_kind, arguments.layer, arguments)
        for removed_fraction in arguments.removed_fractions:
            keep = importance.topk(width - round(removed_fraction * width)).indices.sort().values
            sliced = pruned_mlp(original_mlp, keep)
            fitted = pruned_mlp(original_mlp, keep, statistics.down_weight(keep, arguments.relative_ridge).float())
            for variant, mlp in (("sliced", sliced), ("least_squares", fitted), ("trained", None)):
                if (importance_kind, removed_fraction, variant) in done:
                    continue
                start = time.perf_counter()
                extra: dict[str, float | int | list[float]] = {}
                if mlp is None:
                    mlp = copy.deepcopy(fitted)
                    extra = train_through_next_layer(
                        model,
                        arguments.layer,
                        mlp,
                        arguments.data_directory / f"layer-{arguments.layer:02d}-pairs",
                        arguments,
                    )
                row = {
                    "importance": importance_kind,
                    "removed_fraction": removed_fraction,
                    "variant": variant,
                    "kept_neurons": keep.numel(),
                    **evaluate(model, arguments.layer, mlp, measurement_ids, wikitext_ids, arguments, evaluation_sets),
                    **extra,
                    "seconds": time.perf_counter() - start,
                }
                with results_path.open("a") as results_file:
                    results_file.write(json.dumps(row) + "\n")
                log_event(output, {"step": "variant", **row})
    log_event(output, {"step": "done"})


if __name__ == "__main__":
    main()
