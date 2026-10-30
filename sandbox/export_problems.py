import json
import sys
from pathlib import Path

from evalplus.data import get_human_eval_plus, get_mbpp_plus


def jsonl(rows: list[dict[str, str]]) -> str:
    return "".join(json.dumps(row) + "\n" for row in rows)


def main() -> None:
    output_directory = Path(sys.argv[1])
    for dataset, problems in (("humaneval", get_human_eval_plus()), ("mbpp", get_mbpp_plus())):
        rows = [
            {"task_id": task_id, "prompt": problem["prompt"], "entry_point": problem["entry_point"]}
            for task_id, problem in problems.items()
        ]
        reference_solutions = [
            {"task_id": task_id, "solution": problem["prompt"] + problem["canonical_solution"]}
            for task_id, problem in problems.items()
        ]
        (output_directory / f"{dataset}-problems.jsonl").write_text(jsonl(rows))
        (output_directory / f"{dataset}-reference-solutions.jsonl").write_text(jsonl(reference_solutions))


if __name__ == "__main__":
    main()
