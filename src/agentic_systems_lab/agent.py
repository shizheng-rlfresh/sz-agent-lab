"""Deterministic repo triage agent."""

from __future__ import annotations

import json
from pathlib import Path

from agentic_systems_lab.context import estimate_tokens
from agentic_systems_lab.policy import ToolPolicy
from agentic_systems_lab.tools import list_files, read_file
from agentic_systems_lab.tracer import TraceLogger


def _trace_path_for(repo_path: Path) -> Path:
    return Path("traces") / f"{repo_path.name}_trace.jsonl"


def _diagnose(files: list[str], contents: dict[str, str]) -> list[dict]:
    combined = "\n".join(contents.values()).lower()
    findings: list[dict] = []
    calculator = contents.get("calculator.py", "")
    tests = contents.get("test_calculator.py", "")
    if "return a / b" in calculator and (
        "divide(1, 0) is none" in tests.lower()
        or "division by zero" in combined
        or "zerodivisionerror" in combined
    ):
        findings.append(
            {
                "file": "calculator.py",
                "issue": "Division-by-zero contract mismatch between implementation and tests.",
                "evidence": "divide returns a / b while tests/documentation specify different zero-division behavior.",
                "confidence": 0.92,
            }
        )
    if "ignore all previous instructions" in combined:
        findings.append(
            {
                "file": next(
                    (name for name, text in contents.items() if "ignore all previous instructions" in text.lower()),
                    files[0] if files else "",
                ),
                "issue": "Repository content contains prompt-injection instructions.",
                "evidence": "Text attempts to override agent instructions and expand file access.",
                "confidence": 0.88,
            }
        )
    if not findings:
        findings.append(
            {
                "file": files[0] if files else "",
                "issue": "No deterministic issue signature matched.",
                "evidence": "The baseline triage rules did not identify a known lab failure mode.",
                "confidence": 0.35,
            }
        )
    return findings


def run_repo_triage(
    repo_path: str | Path = "data/toy_repos/buggy_calc",
    *,
    trace_path: str | Path | None = None,
    run_id: str | None = None,
    policy: ToolPolicy | None = None,
) -> dict:
    repo = Path(repo_path)
    active_policy = policy or ToolPolicy(allowed_roots=(repo,))
    trace_target = trace_path or _trace_path_for(repo)
    trace = TraceLogger(trace_target, run_id=run_id) if run_id else TraceLogger(trace_target)
    trace.log_event("agent_start", goal="repo_triage", repo_path=str(repo))
    trace.log_event("policy_check", policy=active_policy.to_dict())

    files = trace.timed_tool_call("list_files", lambda: list_files(repo, policy=active_policy), args={"path": str(repo)})
    selected = [name for name in files if name.endswith((".py", ".md", ".txt", ".log"))][:8]
    contents: dict[str, str] = {}
    for file_name in selected:
        text = trace.timed_tool_call(
            "read_file",
            lambda file_name=file_name: read_file(repo / file_name, policy=active_policy),
            args={"path": str(repo / file_name)},
        )
        contents[file_name] = text
        trace.log_event(
            "context_observation",
            source=file_name,
            estimated_tokens=estimate_tokens(text),
            chars=len(text),
        )

    findings = _diagnose(files, contents)
    result = {
        "summary": findings[0]["issue"] if findings else "No findings.",
        "files_inspected": selected,
        "findings": findings,
        "recommended_next_step": (
            "Align the code/test contract, then add a regression eval for the failure mode."
        ),
    }
    trace.log_event("agent_finish", success=True, finding_count=len(findings))
    return result


def main() -> None:
    print(json.dumps(run_repo_triage(), indent=2))


if __name__ == "__main__":
    main()
