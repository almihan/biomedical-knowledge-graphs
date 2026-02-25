#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert JSONL (NDJSON) file to a JSON array file.")
    parser.add_argument("input", type=Path, help="Path to input .jsonl file")
    parser.add_argument("output", type=Path, help="Path to output .json file")
    parser.add_argument(
        "--indent",
        type=int,
        default=None,
        help="Pretty-print indentation (example: --indent 2)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    records = []
    with args.input.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            text = line.strip()
            if not text:
                continue
            try:
                records.append(json.loads(text))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_no}: {exc}") from exc

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=args.indent)
        if args.indent is not None:
            f.write("\n")

    print(f"Wrote {len(records)} records to {args.output}")


if __name__ == "__main__":
    main()

"""
python3 scripts/jsonl_to_json.py entity_relation_index_ovary.jsonl docs/graph.json --indent 2
"""