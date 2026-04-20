from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Single query payload for the lightweight service endpoint."""

    query: str = Field(
        min_length=1, description="User query to send to the LLM endpoint")


class LLMResponse(BaseModel):
    """Response returned by the mock LLM endpoint."""
    status_code: int = Field(default=200, ge=100, le=599)
    response: str = Field(description="Text returned by the endpoint")


class ErrorResponse(BaseModel):
    """Standard API error payload."""
    status_code: int = Field(default=500, ge=100, le=599)
    detail: str = Field(min_length=1)


class TestCase(BaseModel):
    """One JSONL test record used for evaluation runs."""

    id: str = Field(
        min_length=1, description="Unique identifier for the test case")
    input: str = Field(min_length=1, description="Input prompt/question")
    expected: str = Field(min_length=1, description="Expected answer text")


class Verdict(str, Enum):
    """Allowed scoring verdicts."""

    PASS = "pass"
    PARTIAL = "partial"
    FAIL = "fail"


class ScoreResult(BaseModel):
    """Evaluation output for one test case."""

    exact_match: float = Field(ge=0.0, le=1.0)
    similarity: float = Field(ge=0.0, le=1.0)
    verdict: Verdict
    reason: str = Field(min_length=1)


class EvaluatedCase(BaseModel):
    """Full details for a single evaluated case, including failures/anomalies."""

    case_id: str = Field(min_length=1)
    input: str = Field(min_length=1)
    expected: str = Field(min_length=1)
    response: str | None = Field(
        default=None, description="Raw response from the LLM endpoint")
    score: ScoreResult | None
    error: str | None = Field(
        default=None, description="Endpoint or processing error")


class RunSummary(BaseModel):
    """Aggregate report for an evaluation run."""

    total_cases: int = Field(ge=0)
    passed: int = Field(ge=0)
    partial: int = Field(ge=0)
    failed: int = Field(ge=0)
    pass_rate: float = Field(ge=0.0, le=1.0)
    started_at: datetime
    completed_at: datetime
    cases: list[EvaluatedCase] = Field(default_factory=list)
