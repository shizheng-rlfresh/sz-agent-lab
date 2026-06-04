from agentic_systems_lab.evals import EvalTask, evaluate_result


VALID_RESULT = {
    "summary": "Division by zero contract mismatch.",
    "files_inspected": ["calculator.py", "test_calculator.py"],
    "findings": [
        {
            "file": "calculator.py",
            "issue": "Division by zero raises instead of returning None.",
            "evidence": "return a / b",
            "confidence": 0.9,
        }
    ],
    "recommended_next_step": "Align implementation and test contract.",
}


def test_evaluate_result_passes_expected_schema_file_and_keyword() -> None:
    task = EvalTask(
        name="buggy_calc",
        repo_path="data/toy_repos/buggy_calc",
        expected_file="calculator.py",
        expected_keyword="division",
    )

    result = evaluate_result(task, VALID_RESULT, invalid_tool_call_count=0)

    assert result["schema_ok"] is True
    assert result["expected_file_inspected"] is True
    assert result["expected_keyword_present"] is True
    assert result["hallucinated_file_count"] == 0
    assert result["invalid_tool_call_count"] == 0
    assert result["passed"] is True


def test_evaluate_result_counts_hallucinated_files_and_failures() -> None:
    task = EvalTask(
        name="buggy_calc",
        repo_path="data/toy_repos/buggy_calc",
        expected_file="calculator.py",
        expected_keyword="division",
        allowed_files=("calculator.py", "test_calculator.py"),
    )
    bad = dict(VALID_RESULT)
    bad["files_inspected"] = ["missing.py"]

    result = evaluate_result(task, bad, invalid_tool_call_count=1)

    assert result["expected_file_inspected"] is False
    assert result["hallucinated_file_count"] == 1
    assert result["invalid_tool_call_count"] == 1
    assert result["passed"] is False
