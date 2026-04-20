from app.loader import load_jsonl


def test_load_jsonl_returns_test_cases(tmp_path):
    test_file = tmp_path / "cases.jsonl"
    test_file.write_text(
        '{"id": "q1", "input": "What is the leave policy?", "expected": "14 days annual leave"}\n'
        '{"id": "q2", "input": "Who approves travel claims?", "expected": "Direct manager"}\n',
        encoding="utf-8",
    )

    test_cases = list(load_jsonl(test_file))

    assert len(test_cases) == 2
    assert test_cases[0].id == "q1"
    assert test_cases[0].input == "What is the leave policy?"
    assert test_cases[0].expected == "14 days annual leave"
    assert test_cases[1].id == "q2"
