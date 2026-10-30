import itertools
from collections.abc import Iterable, Iterator
from pathlib import Path

import torch
from datasets import load_dataset
from transformers import PreTrainedTokenizerBase

CODE_LANGUAGES = ("Python", "JavaScript", "Java", "C++", "C", "C#", "PHP")
CODE_PARQUET_URL = (
    "hf://datasets/codeparrot/github-code-clean@refs%2Fconvert%2Fparquet/{language}-all/partial-train/0000.parquet"
)
MINIMUM_TEXT_CHARACTERS = 200


def stream_c4_texts(seed: int) -> Iterator[str]:
    dataset = load_dataset("allenai/c4", "en", split="validation", streaming=True)
    for row in dataset.shuffle(seed=seed, buffer_size=10_000):
        if len(row["text"]) >= MINIMUM_TEXT_CHARACTERS:
            yield row["text"]


def stream_code_texts(seed: int, languages: tuple[str, ...] = CODE_LANGUAGES) -> Iterator[str]:
    language_streams = [
        iter(
            load_dataset(
                "parquet", data_files=CODE_PARQUET_URL.format(language=language), split="train", streaming=True
            ).shuffle(seed=seed, buffer_size=2_000)
        )
        for language in languages
    ]
    for language_stream in itertools.cycle(language_streams):
        row = next(language_stream)
        if len(row["code"]) >= MINIMUM_TEXT_CHARACTERS:
            yield row["code"]


def pack_sequences(
    tokenizer: PreTrainedTokenizerBase, texts: Iterable[str], sequence_length: int, sequence_count: int
) -> torch.Tensor:
    separator = [tokenizer.eos_token_id]
    buffer: list[int] = []
    sequences: list[list[int]] = []
    for text in texts:
        buffer.extend(tokenizer(text, add_special_tokens=False)["input_ids"] + separator)
        while len(buffer) >= sequence_length and len(sequences) < sequence_count:
            sequences.append(buffer[:sequence_length])
            buffer = buffer[sequence_length:]
        if len(sequences) == sequence_count:
            break
    return torch.tensor(sequences, dtype=torch.long)


def interleave_sources(
    text_sequences: torch.Tensor, code_sequences: torch.Tensor, text_per_code: int
) -> tuple[torch.Tensor, list[str]]:
    rows: list[torch.Tensor] = []
    sources: list[str] = []
    text_index = 0
    for code_index in range(code_sequences.shape[0]):
        for _ in range(text_per_code):
            rows.append(text_sequences[text_index])
            sources.append("c4")
            text_index += 1
        rows.append(code_sequences[code_index])
        sources.append("code")
    return torch.stack(rows), sources


def build_measurement_set(
    tokenizer: PreTrainedTokenizerBase, sequence_count: int, sequence_length: int, text_per_code: int, seed: int
) -> tuple[torch.Tensor, list[str]]:
    group_size = text_per_code + 1
    code_count = sequence_count // group_size
    text_sequences = pack_sequences(tokenizer, stream_c4_texts(seed), sequence_length, code_count * text_per_code)
    code_sequences = pack_sequences(tokenizer, stream_code_texts(seed), sequence_length, code_count)
    return interleave_sources(text_sequences, code_sequences, text_per_code)


def load_or_build_measurement_set(
    path: Path,
    tokenizer: PreTrainedTokenizerBase,
    sequence_count: int,
    sequence_length: int,
    text_per_code: int,
    seed: int,
) -> tuple[torch.Tensor, list[str]]:
    if path.exists():
        stored = torch.load(path)
        return stored["token_ids"], stored["sources"]
    token_ids, sources = build_measurement_set(tokenizer, sequence_count, sequence_length, text_per_code, seed)
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"token_ids": token_ids, "sources": sources, "seed": seed}, path)
    return token_ids, sources


def interleave_evenly(sources: dict[str, torch.Tensor]) -> tuple[torch.Tensor, list[str]]:
    positions = sorted(
        ((index + 0.5) / rows.shape[0], name, index) for name, rows in sources.items() for index in range(rows.shape[0])
    )
    return torch.stack([sources[name][index] for _, name, index in positions]), [name for _, name, _ in positions]


def build_disjoint_sets(
    tokenizer: PreTrainedTokenizerBase,
    split_counts: dict[str, dict[str, int]],
    sequence_length: int,
    seed: int,
    languages: tuple[str, ...],
) -> dict[str, tuple[torch.Tensor, list[str]]]:
    streams = {"code": stream_code_texts(seed, languages), "c4": stream_c4_texts(seed)}
    totals = {name: sum(counts.get(name, 0) for counts in split_counts.values()) for name in streams}
    packed = {name: pack_sequences(tokenizer, streams[name], sequence_length, totals[name]) for name in streams}
    offsets = dict.fromkeys(streams, 0)
    result = {}
    for split, counts in split_counts.items():
        parts = {}
        for name, count in counts.items():
            parts[name] = packed[name][offsets[name] : offsets[name] + count]
            offsets[name] += count
        result[split] = interleave_evenly(parts)
    return result
