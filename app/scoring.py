"""
Module to perform scoring of LLM responses against expected outputs.
"""
import string

from .schemas import ScoreResult, Verdict


class Scorer:
    """Class to encapsulate scoring logic for LLM responses."""

    def __init__(self, partial_threshold: float = 0.5):
        """
        Initialize the scorer with a partial match threshold.

        Args:
            partial_threshold (float): The similarity threshold for a partial match.
        """
        self.partial_threshold = partial_threshold

    def __call__(self, expected: str, response: str) -> ScoreResult:
        return self.score(expected, response)

    def score(self, expected: str, response: str) -> ScoreResult:
        """Calculate scores and verdict for a single test case."""
        exact_match = self._exact_match_score(expected, response)
        similarity = self._similarity_score(expected, response)

        if exact_match == 1.0:
            verdict = Verdict.PASS
            reason = "Exact match"
        elif similarity >= self.partial_threshold:
            verdict = Verdict.PARTIAL
            reason = f"Similarity {similarity:.2f} above threshold"
        else:
            verdict = Verdict.FAIL
            reason = f"Similarity {similarity:.2f} below threshold"

        return ScoreResult(
            exact_match=exact_match,
            similarity=similarity,
            verdict=verdict,
            reason=reason,

        )

    def _exact_match_score(self, expected: str, response: str) -> float:
        """Calculate exact match score (1.0 for exact match, else 0.0)."""
        return 1.0 if self._normalise_text(expected) == self._normalise_text(response) else 0.0

    def _similarity_score(self, expected: str, response: str) -> float:
        """Calculate a simple similarity score based on token(word) overlap."""
        expected_tokens = set(self._normalise_text(expected).split())
        response_tokens = set(self._normalise_text(response).split())
        if not expected_tokens:
            return 0.0
        overlap = expected_tokens.intersection(response_tokens)
        return len(overlap) / len(expected_tokens)

    def _normalise_text(self, text: str) -> str:
        """
        Normalise test
        1. Lowercase
        2. Remove punctuation
        3. Remove trailing and leading whitespace
        """
        if not isinstance(text, str):
            return ""

        text = text.lower()
        text = text.translate(str.maketrans("", "", string.punctuation))
        text = text.strip()
        return text
