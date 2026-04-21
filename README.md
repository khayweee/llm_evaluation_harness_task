# LLM Evaluation Harness

## Folder Structure

```
llm_eval_harness/
├── app/
│   ├── main.py          # CLI entrypoint
│   ├── loader.py        # read/validate JSONL
│   ├── endpoint.py      # mock endpoint client / dummy model call
│   ├── scoring.py       # exact match + token overlap
│   ├── evaluator.py     # orchestrates one full run
│   └── schemas.py       # dataclasses / pydantic models
├── tests/
│   └── test_scoring.py
├── data/
│   └── sample.jsonl
├── outputs/
│   └── report.json
├── README.md
└── requirements.txt
```

```bash
pip install -r requirements.txt
```

## Run Evaluation

```python
INPUT_FILE=test.jsonl
OUTPUT_FILE=outputs/report.json

python -m app.main \
    --input "$INPUT_FILE" \
    --output "$OUTPUT_FILE" \
    --partial_threshold 0.5 \
    --random_seed 42 \
    --verdict_points pass=3,partial=1,fail=0 \
```

Script output:

```text
Loaded test case from line 1
... Skipping line 2 due to JSON decoding error: Expecting value: line 1 column 7 (char 6)
Loaded test case from line 3
```

### Evaluation Report

```json
{
  "total_cases": 2,
  "passed": 1,
  "partial": 0,
  "failed": 1,
  "pass_rate": 0.5,
  "started_at": "2026-04-20T21:13:39.597352",
  "completed_at": "2026-04-20T21:13:39.597580",
  "cases": [
    {
      "case_id": "q1",
      "input": "What is the leave policy?",
      "expected": "14 days annual leave",
      "response": "14 days annual leave",
      "score": {
        "exact_match": 1.0,
        "similarity": 1.0,
        "verdict": "pass",
        "reason": "Exact match"
      },
      "error": null
    },
    {
      "case_id": "q3",
      "input": "Who approves insurance claims?",
      "expected": "HR",
      "response": "",
      "score": {
        "exact_match": 0.0,
        "similarity": 0.0,
        "verdict": "fail",
        "reason": "Similarity 0.00 below threshold"
      },
      "error": null
    }
  ]
}
```

## Dev: Run Tests

```bash
python -m pytest -v --tb=short
```

```bash
============================= test session starts ==============================
collected 8 items

tests/integration/test_endpoint.py::test_model_endpoint_returns_valid_response_for_known_query PASSED           [ 12%]
tests/integration/test_endpoint.py::test_model_endpoint_returns_fallback_response_for_unknown_query PASSED      [ 25%]
tests/unit/test_loader.py::test_load_jsonl_returns_test_cases PASSED                                            [ 37%]
tests/unit/test_scoring.py::test_exact_match_score PASSED                                                       [ 50%]
tests/unit/test_scoring.py::test_similarity_score PASSED                                                        [ 62%]
tests/unit/test_scoring.py::test_score_returns_pass_verdict PASSED                                              [ 75%]
tests/unit/test_scoring.py::test_score_returns_partial_verdict PASSED                                           [ 87%]
tests/unit/test_scoring.py::test_score_returns_fail_verdict PASSED                                              [100%]

============================== 8 passed in 0.07s ===============================
```

## Future Scoring Improvements

With more time, I would improve the scoring metric beyond exact match and token
overlap so the harness can evaluate open-ended answers more reliably:

1. **BERTScore**:

   > Compare the generated `response` against the `expected` answer at
   > the contextual token level. This would show whether individual tokens and
   > phrases are similar even when the wording is not exactly the same.

2. **Embedding similarity**:

   > Compare vector embeddings for the `response` and
   > `expected` answer to measure their semantic similarity. This is probably the
   > more important metric for open-ended question-answering tasks, which is
   > similar to TruthfulQA-style evaluations.
   > Correct answer can use different wording while still preserving the same meaning.
