from __future__ import annotations
from datetime import datetime
from pathlib import Path

from .endpoint import model_endpoint
from .loader import load_jsonl
from .scoring import Scorer
from .schemas import ErrorResponse, EvaluatedCase, LLMResponse, QueryRequest, RunSummary, ScoreResult


def build_run_summary(
        cases: list[EvaluatedCase],
        started_at: datetime,
        completed_at: datetime,
        verdict_points: dict[str, int],
) -> RunSummary:
    total_cases = len(cases)
    passed = sum(1 for c in cases if c.score and c.score.verdict == "pass")
    partial = sum(1 for c in cases if c.score and c.score.verdict == "partial")
    failed = sum(1 for c in cases if c.score and c.score.verdict == "fail")
    pass_rate = (passed * verdict_points['pass'] + partial * verdict_points['partial'] + failed *
                 verdict_points['fail']) / (total_cases * max(verdict_points.values())) if total_cases > 0 else 0.0

    return RunSummary(
        total_cases=total_cases,
        passed=passed,
        partial=partial,
        failed=failed,
        pass_rate=pass_rate,
        started_at=started_at,
        completed_at=completed_at,
        cases=cases,
    )


def evaluate_run(input_path: Path,
                 verdict_points: dict[str, int] = {
                     "pass": 3, "partial": 1, "fail": 0},
                 random_seed: int = 42,
                 partial_threshold: float = 0.5) -> RunSummary:
    started_at = datetime.now()
    evaluated_cases = []
    scorer = Scorer(partial_threshold=partial_threshold)

    for case in load_jsonl(input_path):
        try:
            request = QueryRequest(query=case.input)
            llm_response: LLMResponse | ErrorResponse = model_endpoint(
                request, random_seed=random_seed)
            if llm_response.status_code != 200:
                raise Exception(f"Model endpoint error: {llm_response}")
            score: ScoreResult = scorer(case.expected, llm_response.response)
            evaluated_cases.append(
                EvaluatedCase(
                    case_id=case.id,
                    input=case.input,
                    expected=case.expected,
                    response=llm_response.response,
                    score=score,
                    error=None,
                )
            )
        except Exception as exc:
            evaluated_cases.append(
                EvaluatedCase(
                    case_id=case.id,
                    input=case.input,
                    expected=case.expected,
                    response=None,
                    score=None,
                    error=str(exc),
                )
            )
    ended_at = datetime.now()
    return build_run_summary(
        cases=evaluated_cases,
        started_at=started_at,
        completed_at=ended_at,
        verdict_points=verdict_points,
    )
