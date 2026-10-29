import argparse
import json
import time
from pathlib import Path

import torch
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, PreTrainedModel

from qwen_compression.activations import collect_neuron_statistics
from qwen_compression.data import load_or_build_measurement_set
from qwen_compression.importance import fisher_kl_coefficients
from qwen_compression.perturbation import measure_perturbations

MODEL_NAME = "Qwen/Qwen3-0.6B-Base"
DELTAS = (-1.0, -0.5, 0.5, 1.0)
DTYPES = {"bfloat16": torch.bfloat16, "float32": torch.float32}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", nargs="+", default=["data", "statistics", "precision", "exact", "noise", "fisher"])
    parser.add_argument("--dtype", choices=DTYPES, default="bfloat16")
    parser.add_argument("--layers", type=int, nargs="+", default=[2, 13, 25])
    parser.add_argument("--sequence-count", type=int, default=64)
    parser.add_argument("--sequence-length", type=int, default=2048)
    parser.add_argument("--measurement-sequences", type=int, default=8)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--chunk-length", type=int, default=256)
    parser.add_argument("--precision-neurons", type=int, default=64)
    parser.add_argument("--noise-neurons", type=int, default=500)
    parser.add_argument("--fisher-samples", type=int, default=16)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--data-path", type=Path, default=Path.home() / "qwen3-checkpoints/phase2/measurement-set.pt")
    parser.add_argument("--output", type=Path, default=Path("results/phase2/stage1"))
    return parser.parse_args()


def load_model(dtype: torch.dtype) -> PreTrainedModel:
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, dtype=dtype, device_map="cuda").eval()
    model.requires_grad_(False)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    return model


def log_event(output: Path, record: dict[str, object]) -> None:
    record = {"time": time.strftime("%Y-%m-%d %H:%M:%S"), **record}
    with (output / "log.jsonl").open("a") as log_file:
        log_file.write(json.dumps(record) + "\n")
    print(json.dumps(record), flush=True)


def all_perturbations(width: int) -> tuple[torch.Tensor, torch.Tensor]:
    neuron_indices = torch.arange(width).repeat_interleave(len(DELTAS))
    scales = (1 + torch.tensor(DELTAS)).repeat(width)
    return neuron_indices, scales


def run_statistics(model: PreTrainedModel, token_ids: torch.Tensor, output: Path) -> None:
    statistics = collect_neuron_statistics(model, token_ids, active_threshold=1e-2)
    torch.save(statistics, output / "statistics.pt")


def run_precision(
    arguments: argparse.Namespace, token_ids: torch.Tensor, output: Path, generator: torch.Generator
) -> None:
    neuron_indices = torch.randint(0, 3072, (arguments.precision_neurons,), generator=generator)
    controls = torch.ones(arguments.precision_neurons)
    disabled = torch.zeros(arguments.precision_neurons)
    weakened = torch.full((arguments.precision_neurons,), 0.5)
    indices = torch.cat([neuron_indices, neuron_indices, neuron_indices])
    scales = torch.cat([controls, disabled, weakened])
    results: dict[str, object] = {"neuron_indices": neuron_indices, "scales": scales, "layer": arguments.layers[1]}
    for dtype_name, dtype in DTYPES.items():
        model = load_model(dtype)
        start = time.perf_counter()
        kl, loss_change = measure_perturbations(
            model, token_ids, arguments.layers[1], indices, scales, arguments.batch_size, arguments.chunk_length
        )
        results[f"kl_{dtype_name}"] = kl
        results[f"loss_change_{dtype_name}"] = loss_change
        log_event(output, {"step": "precision", "dtype": dtype_name, "seconds": time.perf_counter() - start})
        del model
        torch.cuda.empty_cache()
    torch.save(results, output / "precision.pt")


def run_exact(model: PreTrainedModel, arguments: argparse.Namespace, token_ids: torch.Tensor, output: Path) -> None:
    neuron_indices, scales = all_perturbations(model.config.intermediate_size)
    for layer_index in arguments.layers:
        path = output / f"exact-layer-{layer_index:02d}.pt"
        if path.exists():
            continue
        start = time.perf_counter()
        kl, loss_change = measure_perturbations(
            model, token_ids, layer_index, neuron_indices, scales, arguments.batch_size, arguments.chunk_length
        )
        width = model.config.intermediate_size
        torch.save(
            {
                "kl": kl.view(width, len(DELTAS), -1),
                "loss_change": loss_change.view(width, len(DELTAS), -1),
                "deltas": DELTAS,
            },
            path,
        )
        log_event(output, {"step": "exact", "layer": layer_index, "seconds": time.perf_counter() - start})


def run_noise(
    model: PreTrainedModel,
    arguments: argparse.Namespace,
    second_token_ids: torch.Tensor,
    output: Path,
    generator: torch.Generator,
) -> None:
    per_layer = arguments.noise_neurons // len(arguments.layers)
    results: dict[str, object] = {"deltas": DELTAS}
    for layer_index in arguments.layers:
        neurons = torch.randperm(model.config.intermediate_size, generator=generator)[:per_layer]
        neuron_indices = neurons.repeat_interleave(len(DELTAS))
        scales = (1 + torch.tensor(DELTAS)).repeat(per_layer)
        start = time.perf_counter()
        kl, loss_change = measure_perturbations(
            model, second_token_ids, layer_index, neuron_indices, scales, arguments.batch_size, arguments.chunk_length
        )
        results[f"layer_{layer_index}"] = {
            "neurons": neurons,
            "kl": kl.view(per_layer, len(DELTAS), -1),
            "loss_change": loss_change.view(per_layer, len(DELTAS), -1),
        }
        log_event(output, {"step": "noise", "layer": layer_index, "seconds": time.perf_counter() - start})
    torch.save(results, output / "noise.pt")


def run_fisher(
    model: PreTrainedModel,
    arguments: argparse.Namespace,
    token_ids: torch.Tensor,
    output: Path,
) -> None:
    generator = torch.Generator(device="cuda").manual_seed(arguments.seed)
    start = time.perf_counter()
    coefficients = fisher_kl_coefficients(model, token_ids, arguments.fisher_samples, generator)
    torch.save({"coefficients": coefficients, "samples_per_sequence": arguments.fisher_samples}, output / "fisher.pt")
    log_event(output, {"step": "fisher", "seconds": time.perf_counter() - start})


def main() -> None:
    arguments = parse_arguments()
    output = arguments.output
    output.mkdir(parents=True, exist_ok=True)
    generator = torch.Generator().manual_seed(arguments.seed)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    token_ids, sources = load_or_build_measurement_set(
        arguments.data_path, tokenizer, arguments.sequence_count, arguments.sequence_length, 3, arguments.seed
    )
    measured = token_ids[: arguments.measurement_sequences]
    second = token_ids[arguments.measurement_sequences : 2 * arguments.measurement_sequences]
    log_event(
        output,
        {
            "step": "start",
            "arguments": {key: str(value) for key, value in vars(arguments).items()},
            "torch": torch.__version__,
            "transformers": transformers.__version__,
            "sources_measured": sources[: arguments.measurement_sequences],
        },
    )
    if "precision" in arguments.steps and not (output / "precision.pt").exists():
        run_precision(arguments, measured[:1], output, generator)
    needs_model = {"statistics", "exact", "noise", "fisher"} & set(arguments.steps)
    if not needs_model:
        return
    model = load_model(DTYPES[arguments.dtype])
    if "statistics" in arguments.steps and not (output / "statistics.pt").exists():
        start = time.perf_counter()
        run_statistics(model, measured, output)
        log_event(output, {"step": "statistics", "seconds": time.perf_counter() - start})
    if "exact" in arguments.steps:
        run_exact(model, arguments, measured, output)
    if "noise" in arguments.steps and not (output / "noise.pt").exists():
        run_noise(model, arguments, second, output, generator)
    if "fisher" in arguments.steps and not (output / "fisher.pt").exists():
        run_fisher(model, arguments, measured, output)
    log_event(output, {"step": "done"})


if __name__ == "__main__":
    main()
