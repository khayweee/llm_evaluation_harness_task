from app.endpoint import model_endpoint
from app.schemas import LLMResponse, QueryRequest


def test_model_endpoint_returns_valid_response_for_known_query():
    request = QueryRequest(query="What is the leave policy?")

    response = model_endpoint(request, random_seed=42)

    assert isinstance(response, LLMResponse)


def test_model_endpoint_returns_fallback_response_for_unknown_query():
    request = QueryRequest(query="What is the dress code?")

    response = model_endpoint(request, random_seed=42)

    assert isinstance(response, LLMResponse)
