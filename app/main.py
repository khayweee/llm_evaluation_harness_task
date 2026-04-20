import argparse
import sys
from pathlib import Path
from .evaluator import evaluate_run


VALID_VERDICTS = {"pass", "partial", "fail"}


def parse_verdict_points(s: str) -> dict[str, int]:
    try:
        pairs = s.split(",")
        verdict_points = {}
        for pair in pairs:
            verdict, points = pair.split("=", maxsplit=1)
            verdict = verdict.strip().lower()
            points = int(points.strip())
            if verdict not in VALID_VERDICTS:
                raise argparse.ArgumentTypeError(
                    f"Invalid verdict '{verdict}' in verdict points. Allowed values are: {VALID_VERDICTS}")

            if points < 0:
                raise argparse.ArgumentTypeError(
                    f"Points for verdict '{verdict}' must be non-negative")

            verdict_points[verdict] = points
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"Invalid format for verdict points: {s}. Expected format: pass=3,partial=1,fail=0") from exc

    missing = VALID_VERDICTS - verdict_points.keys()
    if missing:
        raise argparse.ArgumentTypeError(
            f"Missing verdict point values for: {', '.join(sorted(missing))}"
        )

    return verdict_points


def parse_args():
    parser = argparse.ArgumentParser(description="LLM Evaluation Harness")

    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to the input JSONL file containing test cases",
    )

    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Path to the output JSON file for evaluation results",
    )

    parser.add_argument(
        "--random_seed",
        type=int,
        default=None,
        help="Random seed for reproducibility (default: None)",
    )
    parser.add_argument(
        "--partial_threshold",
        type=float,
        default=0.5,
        help="Similarity threshold for partial credit (default: 0.5)",
    )
    parser.add_argument(
        "--verdict_points",
        type=parse_verdict_points,
        default={"pass": 3, "partial": 1, "fail": 0},
        help="Comma-separated verdict point values in the format pass=3,partial=1,fail=0 (default: pass=3,partial=1,fail=0)",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.is_file():
        print(f"Error: Input file {input_path} does not exist.")
        sys.exit(1)

    try:
        run_summary = evaluate_run(
            input_path,
            random_seed=args.random_seed,
            partial_threshold=args.partial_threshold,
            verdict_points=args.verdict_points)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            run_summary.model_dump_json(indent=2),
            encoding="utf-8",
        )
    except Exception as e:
        print(f"Error loading test cases: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
