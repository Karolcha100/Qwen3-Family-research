import json
import math
import time
from pathlib import Path
from typing import cast

import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers._typing import GenerativePreTrainedModel

BASE_MODEL = "Qwen/Qwen3-0.6B-Base"
INSTRUCT_MODEL = "Qwen/Qwen3-0.6B"
CONTEXT_LENGTH = 2048
MATRIX_SIZE = 4096
MATMUL_REPEATS = 50
RESULTS_PATH = Path("results/phase1-smoke-test.jsonl")


def measure_bf16_matmul_tflops() -> float:
    left = torch.randn(MATRIX_SIZE, MATRIX_SIZE, device="cuda", dtype=torch.bfloat16)
    right = torch.randn(MATRIX_SIZE, MATRIX_SIZE, device="cuda", dtype=torch.bfloat16)
    _ = left @ right
    torch.cuda.synchronize()
    start = time.perf_counter()
    for _ in range(MATMUL_REPEATS):
        _ = left @ right
    torch.cuda.synchronize()
    elapsed = time.perf_counter() - start
    return MATMUL_REPEATS * 2 * MATRIX_SIZE**3 / elapsed / 1e12


def generate_answer(question: str) -> dict[str, str | float | int]:
    tokenizer = AutoTokenizer.from_pretrained(INSTRUCT_MODEL)
    model = cast(
        GenerativePreTrainedModel,
        AutoModelForCausalLM.from_pretrained(INSTRUCT_MODEL, dtype=torch.bfloat16, device_map="cuda"),
    )
    prompt = tokenizer.apply_chat_template(
        [{"role": "user", "content": question}], tokenize=False, add_generation_prompt=True, enable_thinking=False
    )
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    start = time.perf_counter()
    output = model.generate(**inputs, max_new_tokens=96, do_sample=False)
    elapsed = time.perf_counter() - start
    new_tokens = output[0, inputs["input_ids"].shape[1] :]
    return {
        "question": question,
        "answer": tokenizer.decode(new_tokens, skip_special_tokens=True),
        "new_tokens": int(new_tokens.shape[0]),
        "tokens_per_second": new_tokens.shape[0] / elapsed,
    }


@torch.no_grad()
def wikitext2_perplexity(model_name: str) -> dict[str, float | int]:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, dtype=torch.bfloat16, device_map="cuda")
    text = "\n\n".join(load_dataset("Salesforce/wikitext", "wikitext-2-raw-v1", split="test")["text"])
    token_ids = tokenizer(text, return_tensors="pt").input_ids
    window_count = token_ids.shape[1] // CONTEXT_LENGTH
    negative_log_likelihood_sum = 0.0
    start = time.perf_counter()
    for window_index in range(window_count):
        window = token_ids[:, window_index * CONTEXT_LENGTH : (window_index + 1) * CONTEXT_LENGTH].to("cuda")
        loss = model(window, labels=window).loss.float().item()
        negative_log_likelihood_sum += loss * (CONTEXT_LENGTH - 1)
    elapsed = time.perf_counter() - start
    return {
        "perplexity": math.exp(negative_log_likelihood_sum / (window_count * (CONTEXT_LENGTH - 1))),
        "windows": window_count,
        "tokens": int(token_ids.shape[1]),
        "seconds": elapsed,
        "peak_vram_gib": torch.cuda.max_memory_allocated() / 2**30,
    }


def main() -> None:
    records: list[dict[str, object]] = [
        {
            "test": "environment",
            "torch": torch.__version__,
            "cuda": torch.version.cuda,
            "device": torch.cuda.get_device_name(0),
        },
        {"test": "bf16_matmul", "matrix_size": MATRIX_SIZE, "tflops": measure_bf16_matmul_tflops()},
        {
            "test": "generation",
            "model": INSTRUCT_MODEL,
            **generate_answer("Explain in two sentences what a neural network is."),
        },
    ]
    for model_name in (BASE_MODEL, INSTRUCT_MODEL):
        torch.cuda.reset_peak_memory_stats()
        records.append(
            {
                "test": "wikitext2_perplexity",
                "model": model_name,
                "context_length": CONTEXT_LENGTH,
                **wikitext2_perplexity(model_name),
            }
        )
    RESULTS_PATH.parent.mkdir(exist_ok=True)
    with RESULTS_PATH.open("w") as results_file:
        for record in records:
            results_file.write(json.dumps(record, ensure_ascii=False) + "\n")
            print(json.dumps(record, ensure_ascii=False))


if __name__ == "__main__":
    main()
