import argparse
import difflib
import json
import re
from pathlib import Path
from typing import Any, cast

from datasets import DatasetDict, load_dataset

SIMILARITY_THRESHOLD = 0.9


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-problems", type=Path, default=Path("results/phase2/code-eval/mbpp-problems.jsonl"))
    parser.add_argument("--output-directory", type=Path, default=Path("results/phase2/code-agreement"))
    return parser.parse_args()


def normalized(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def test_description(prompt: str) -> str:
    return prompt.strip().removeprefix('"""').strip().splitlines()[0]


def main() -> None:
    arguments = parse_arguments()
    test_problems = [json.loads(line) for line in arguments.test_problems.read_text().splitlines()]
    test_numbers = {int(problem["task_id"].removeprefix("Mbpp/")) for problem in test_problems}
    test_texts = [normalized(test_description(problem["prompt"])) for problem in test_problems]
    test_entry_points = {problem["entry_point"] for problem in test_problems}
    full = cast(DatasetDict, load_dataset("google-research-datasets/mbpp", "full"))
    rows = sorted(
        (cast(dict[str, Any], row) for split in full.values() for row in split), key=lambda row: row["task_id"]
    )
    kept, excluded = [], {"same_number": 0, "same_text": 0, "similar_text": 0, "same_function_name": 0}
    for row in rows:
        text = normalized(row["text"])
        entry_point = next(
            (name for name in re.findall(r"^def (\w+)", row["code"], re.MULTILINE) if name in row["test_list"][0]), ""
        )
        if row["task_id"] in test_numbers:
            excluded["same_number"] += 1
        elif text in test_texts:
            excluded["same_text"] += 1
        elif (
            max(difflib.SequenceMatcher(None, text, test_text).ratio() for test_text in test_texts)
            >= SIMILARITY_THRESHOLD
        ):
            excluded["similar_text"] += 1
        elif entry_point in test_entry_points:
            excluded["same_function_name"] += 1
        else:
            kept.append(
                {
                    "task_id": f"MbppHeldOut/{row['task_id']}",
                    "prompt": f'"""\n{row["text"].strip()}\n{row["test_list"][0].strip()}\n"""\n',
                    "entry_point": entry_point,
                }
            )
    arguments.output_directory.mkdir(parents=True, exist_ok=True)
    (arguments.output_directory / "mbpp-problems.jsonl").write_text("".join(json.dumps(row) + "\n" for row in kept))
    summary = {"full_mbpp": len(rows), "test_problems": len(test_problems), "kept": len(kept), "excluded": excluded}
    (arguments.output_directory / "set-summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
