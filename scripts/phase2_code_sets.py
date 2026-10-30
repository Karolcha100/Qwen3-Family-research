import argparse
from pathlib import Path

import torch
from transformers import AutoTokenizer

from qwen_compression.data import build_disjoint_sets

MODEL_NAME = "Qwen/Qwen3-0.6B-Base"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--languages", nargs="+", default=["Python"])
    parser.add_argument("--sequence-length", type=int, default=2048)
    parser.add_argument("--seed", type=int, default=2)
    parser.add_argument("--output", type=Path, default=Path.home() / "qwen3-checkpoints/phase2-code")
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    arguments.output.mkdir(parents=True, exist_ok=True)
    split_counts = {
        "measurement-set": {"code": 48, "c4": 16},
        "training-set": {"code": 366, "c4": 122},
        "evaluation-set": {"code": 16, "c4": 16},
    }
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    sets = build_disjoint_sets(
        tokenizer, split_counts, arguments.sequence_length, arguments.seed, tuple(arguments.languages)
    )
    for name, (token_ids, sources) in sets.items():
        torch.save(
            {"token_ids": token_ids, "sources": sources, "seed": arguments.seed, "languages": arguments.languages},
            arguments.output / f"{name}.pt",
        )
        print(name, tuple(token_ids.shape), {source: sources.count(source) for source in set(sources)}, flush=True)


if __name__ == "__main__":
    main()
