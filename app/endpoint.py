import random
from .schemas import QueryRequest, LLMResponse, ErrorResponse
import time


def model_endpoint(query_request: QueryRequest, random_seed: int = 42) -> LLMResponse:
    """Mock LLM endpoint that generates a response based on the input query."""
    if random_seed is not None:
        random.seed(random_seed)
    query = query_request.query
    db = {
        "What is the leave policy?": [
            "14 days annual leave",   # correct
            "14 days",
            "Annual leave is 14 days per year",
            "10 days annual leave"  # incorrect
        ],
        "Who approves travel claims?": [
            "Direct Manager",
            "Manager",
            "Supervisor",
            "HR"
        ]
    }
    if query in db:
        r = random.choice(db[query])
    else:
        responses = [
            "Sorry, I don't have that information.",
            "I am not sure about that.",
            ""
        ]
        r = random.choice(responses)

    if not r:
        ErrorResponse(detail="Model Endpoint Error")
    return LLMResponse(response=r)
