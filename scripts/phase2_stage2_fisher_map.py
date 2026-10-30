import argparse
import json
import time
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM

from qwen_compression.importance import fisher_kl_coefficients

MODEL_NAME = "Qwen/Qwen3-0.6B-Base"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=64)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--data-path", type=Path, default=Path.home() / "qwen3-checkpoints/phase2/measurement-set.pt")
    parser.add_argument("--output", type=Path, default=Path("results/phase2/stage2"))
    return parser.parse_args()


def log_event(output: Path, record: dict[str, object]) -> None:
    record = {"time": time.strftime("%Y-%m-%d %H:%M:%S"), **record}
    with (output / "log.jsonl").open("a") as log_file:
        log_file.write(json.dumps(record) + "\n")
    print(json.dumps(record), flush=True)


def main() -> None:
    arguments = parse_arguments()
    arguments.output.mkdir(parents=True, exist_ok=True)
    path = arguments.output / f"fisher-per-sequence-{arguments.samples}.pt"
    stored = torch.load(arguments.data_path)
    token_ids, sources = stored["token_ids"], stored["sources"]
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, dtype=torch.float32, device_map="cuda").eval()
    model.requires_grad_(False)
    generator = torch.Generator(device="cuda").manual_seed(arguments.seed)
    log_event(arguments.output, {"step": "fisher-start", "samples": arguments.samples, "sequences": len(token_ids)})
    start = time.perf_counter()
    coefficients = torch.stack(
        [fisher_kl_coefficients(model, sequence.unsqueeze(0), arguments.samples, generator) for sequence in token_ids]
    )
    torch.save({"coefficients": coefficients, "sources": sources, "samples_per_sequence": arguments.samples}, path)
    log_event(arguments.output, {"step": "fisher-done", "seconds": time.perf_counter() - start})


if __name__ == "__main__":
    main()
