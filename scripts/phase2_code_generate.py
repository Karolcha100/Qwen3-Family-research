import argparse
import json
import time
from pathlib import Path
from typing import Any, cast

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Qwen3ForCausalLM

from qwen_compression.model_parts import decoder_layers

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
    solutions: dict[str, str] = {}
    generated_tokens = 0
    torch.cuda.reset_peak_memory_stats()
    start = time.perf_counter()
    for batch_start in range(0, len(order), arguments.batch_size):
        task_ids = order[batch_start : batch_start + arguments.batch_size]
        encoded = tokenizer([prompts[task_id] for task_id in task_ids], return_tensors="pt", padding=True).to(
            model.device
        )
        outputs = cast(Any, model).generate(
            **encoded,
            max_new_tokens=arguments.max_new_tokens,
            do_sample=False,
            stop_strings=stop_texts,
            tokenizer=tokenizer,
            pad_token_id=tokenizer.pad_token_id,
        )
        new_tokens = outputs[:, encoded.input_ids.shape[1] :]
        generated_tokens += int((new_tokens != tokenizer.pad_token_id).sum().item())
        for task_id, completion in zip(
            task_ids, tokenizer.batch_decode(new_tokens, skip_special_tokens=True), strict=True
        ):
            solutions[task_id] = prompts[task_id] + truncated(completion, stop_texts)
    seconds = time.perf_counter() - start
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        "".join(json.dumps({"task_id": task_id, "solution": solutions[task_id]}) + "\n" for task_id in prompts)
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
    }
    arguments.output.with_name(arguments.output.name.replace(".jsonl", "-efficiency.json")).write_text(
        json.dumps(efficiency, indent=2)
    )
    print(json.dumps(efficiency, indent=2))


if __name__ == "__main__":
    main()
