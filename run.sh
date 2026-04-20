#!/usr/bin/env bash
set -euo pipefail

INPUT_FILE="${1:-data/test.jsonl}"
OUTPUT_FILE="${2:-outputs/report.json}"
PYTHON_BIN="${PYTHON_BIN:-python}"

if [ -x ".venv/bin/python" ]; then
    PYTHON_BIN=".venv/bin/python"
fi

mkdir -p "$(dirname "$OUTPUT_FILE")"

"$PYTHON_BIN" -m app.main \
    --input "$INPUT_FILE" \
    --output "$OUTPUT_FILE" \
    --partial_threshold 0.5 \
    --random_seed 42 \
    --verdict_points pass=3,partial=1,fail=0 \
