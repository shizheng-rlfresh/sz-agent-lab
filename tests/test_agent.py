import json
from pathlib import Path

from agentic_systems_lab.agent import run_repo_triage
from agentic_systems_lab.policy import ToolPolicy


def make_buggy_calc(root: Path) -> Path:
    repo = root / "buggy_calc"
    repo.mkdir()
    (repo / "calculator.py").write_text(
        "def divide(a, b):\n"
        "    return a / b\n"
    )
    (repo / "test_calculator.py").write_text(
        "import pytest\n"
        "from calculator import divide\n\n"
        "def test_divide_by_zero_returns_none():\n"
        "    assert divide(1, 0) is None\n"
    )
    return repo


def test_repo_triage_agent_returns_structured_diagnosis_and_trace(tmp_path: Path) -> None:
    repo = make_buggy_calc(tmp_path)
    trace_path = tmp_path / "trace.jsonl"
    policy = ToolPolicy(allowed_roots=(repo,))

    result = run_repo_triage(repo, trace_path=trace_path, policy=policy)

    assert set(result) == {"summary", "files_inspected", "findings", "recommended_next_step"}
    assert "calculator.py" in result["files_inspected"]
    assert result["findings"][0]["file"] == "calculator.py"
    assert "division" in result["findings"][0]["issue"].lower()
    assert trace_path.exists()
    trace_types = [json.loads(line)["type"] for line in trace_path.read_text().splitlines()]
    assert trace_types[0] == "agent_start"
    assert "tool_call" in trace_types
    assert trace_types[-1] == "agent_finish"


def test_repo_triage_agent_does_not_mutate_repo(tmp_path: Path) -> None:
    repo = make_buggy_calc(tmp_path)
    before = {path.name: path.read_text() for path in repo.iterdir()}

    run_repo_triage(repo, trace_path=tmp_path / "trace.jsonl", policy=ToolPolicy(allowed_roots=(repo,)))

    after = {path.name: path.read_text() for path in repo.iterdir()}
    assert after == before
