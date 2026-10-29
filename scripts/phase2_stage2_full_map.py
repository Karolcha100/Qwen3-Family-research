import argparse
import json
import time
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, PreTrainedModel

from qwen_compression.perturbation import measure_perturbations, perturbation_grid

MODEL_NAME = "Qwen/Qwen3-0.6B-Base"
DELTAS = (-1.0, -0.5, 0.5, 1.0)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["screened", "exact-all"], required=True)
    parser.add_argument("--top-fraction", type=float, default=0.10)
    parser.add_argument("--random-fraction", type=float, default=0.05)
    parser.add_argument("--measurement-sequences", type=int, nargs="+", default=[0, 3])
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--chunk-length", type=int, default=256)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--data-path", type=Path, default=Path.home() / "qwen3-checkpoints/phase2/measurement-set.pt")
    parser.add_argument("--stage1", type=Path, default=Path("results/phase2/stage1"))
    parser.add_argument("--output", type=Path, default=Path("results/phase2/stage2"))
    return parser.parse_args()


def log_event(output: Path, record: dict[str, object]) -> None:
    record = {"time": time.strftime("%Y-%m-%d %H:%M:%S"), **record}
    with (output / "log.jsonl").open("a") as log_file:
        log_file.write(json.dumps(record) + "\n")
    print(json.dumps(record), flush=True)


def select_neurons(
    mode: str, coefficients: torch.Tensor, top_fraction: float, random_fraction: float, generator: torch.Generator
) -> torch.Tensor:
    width = coefficients.numel()
    if mode == "exact-all":
        return torch.arange(width)
    top = coefficients.topk(int(top_fraction * width)).indices
    remaining = torch.ones(width, dtype=torch.bool)
    remaining[top] = False
    rest = remaining.nonzero().flatten()
    random_rest = rest[torch.randperm(rest.numel(), generator=generator)[: int(random_fraction * width)]]
    return torch.cat([top, random_rest]).sort().values


def load_model() -> PreTrainedModel:
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, dtype=torch.float32, device_map="cuda").eval()
    model.requires_grad_(False)
    return model


def main() -> None:
    arguments = parse_arguments()
    arguments.output.mkdir(parents=True, exist_ok=True)
    generator = torch.Generator().manual_seed(arguments.seed)
    coefficients = torch.load(arguments.stage1 / "fisher.pt")["coefficients"]
    token_ids = torch.load(arguments.data_path)["token_ids"][arguments.measurement_sequences]
    log_event(
        arguments.output, {"step": "start", "arguments": {key: str(value) for key, value in vars(arguments).items()}}
    )
    model = load_model()
    for layer_index in range(coefficients.shape[0]):
        path = arguments.output / f"layer-{layer_index:02d}.pt"
        if path.exists():
            continue
        neurons = select_neurons(
            arguments.mode, coefficients[layer_index], arguments.top_fraction, arguments.random_fraction, generator
        )
        pilot_path = arguments.stage1 / f"exact-layer-{layer_index:02d}.pt"
        start = time.perf_counter()
        if pilot_path.exists():
            pilot = torch.load(pilot_path)
            kl, loss_change = pilot["kl"][neurons], pilot["loss_change"][neurons]
            source = "stage1"
        else:
            neuron_indices, scales = perturbation_grid(neurons, DELTAS)
            flat_kl, flat_loss_change = measure_perturbations(
                model, token_ids, layer_index, neuron_indices, scales, arguments.batch_size, arguments.chunk_length
            )
            kl = flat_kl.view(neurons.numel(), len(DELTAS), -1)
            loss_change = flat_loss_change.view(neurons.numel(), len(DELTAS), -1)
            source = "measured"
        torch.save(
            {"neurons": neurons, "kl": kl, "loss_change": loss_change, "deltas": DELTAS, "mode": arguments.mode}, path
        )
        log_event(
            arguments.output,
            {
                "step": "layer",
                "layer": layer_index,
                "neurons": neurons.numel(),
                "source": source,
                "seconds": time.perf_counter() - start,
            },
        )
    log_event(arguments.output, {"step": "done"})


if __name__ == "__main__":
    main()
