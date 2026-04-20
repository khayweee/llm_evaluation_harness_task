"""
Module to load jsonl files into a list of iterable pydantic models. This is used to load test cases for evaluation runs.
"""
import json
from collections.abc import Iterable
from pathlib import Path
from .schemas import TestCase


def load_jsonl(file_path: Path) -> Iterable[TestCase]:
    """Load a JSONL file and return a list of TestCase objects."""
    with file_path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            try:
                data = json.loads(line)
                print(f"Loaded test case from line {line_number}")
                yield TestCase(**data)
            except json.JSONDecodeError as e:
                print(
                    f"... Skipping line {line_number} due to JSON decoding error: {e}")
            except TypeError as e:
                print(
                    f"Skipping line {line_number} due to error creating TestCase: {e}")
