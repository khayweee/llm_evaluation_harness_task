from app.scoring import Scorer
from app.schemas import ScoreResult, Verdict

scorer = Scorer(partial_threshold=0.5)


def test_exact_match_score():
    assert scorer._exact_match_score("Hello World", "Hello World") == 1.0
    assert scorer._exact_match_score("Hello World", "hello world") == 1.0
    assert scorer._exact_match_score("Hello World!", "Hello World") == 1.0
    assert scorer._exact_match_score("Hello, World", "Hello World") == 1.0
    assert scorer._exact_match_score("Hello World", "Hello") == 0.0
    assert scorer._exact_match_score("Hello World", "Hi there") == 0.0


def test_similarity_score():
    assert scorer._similarity_score("Hello World", "Hello World") == 1.0
    assert scorer._similarity_score("Hello World", "hello world") == 1.0
    assert scorer._similarity_score("Hello World!", "Hello World") == 1.0
    assert scorer._similarity_score("Hello, World", "Hello World") == 1.0
    assert scorer._similarity_score("Hello World", "Hello") == 0.5
    assert scorer._similarity_score("Hello World", "Hi there") == 0.0
    assert scorer._similarity_score("Hello World", "Hi there world") == 0.5


def test_score_returns_pass_verdict():
    result = scorer.score("Hello World", "hello world")

    assert isinstance(result, ScoreResult)
    assert result.verdict is Verdict.PASS


def test_score_returns_partial_verdict():
    result = scorer.score("Hello World", "Hello")

    assert result.verdict is Verdict.PARTIAL


def test_score_returns_fail_verdict():
    result = scorer.score("Hello World", "Hi there")

    assert result.verdict is Verdict.FAIL
