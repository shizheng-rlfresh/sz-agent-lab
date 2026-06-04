from pathlib import Path

from agentic_systems_lab.report import generate_report
from agentic_systems_lab.tracer import TraceLogger


def test_generate_report_includes_trace_eval_policy_context_and_readiness(tmp_path: Path) -> None:
    trace_path = tmp_path / "trace.jsonl"
    logger = TraceLogger(trace_path, run_id="run_test")
    logger.log_event("agent_start")
    logger.log_event("tool_call", tool="read_file", success=True, latency_ms=2)
    eval_results = [{"name": "buggy_calc", "passed": True, "schema_ok": True}]
    context_summary = {
        "total_tokens": 12,
        "cacheable_tokens": 4,
        "dynamic_tokens": 8,
        "large_outputs": [{"name": "log", "tokens": 9}],
    }
    policy_violations = [{"reason": "shell_blocked", "action": "run_shell"}]

    report = generate_report(
        trace_path=trace_path,
        eval_results=eval_results,
        context_summary=context_summary,
        policy_violations=policy_violations,
    )

    assert "# Agentic Systems Lab Report" in report
    assert "Trace Summary" in report
    assert "Eval Results" in report
    assert "Policy Warnings" in report
    assert "Context Growth" in report
    assert "Production Readiness" in report
    assert "shell_blocked" in report


def test_generate_report_includes_deployment_recommendation() -> None:
    report = generate_report(
        eval_results=[
            {"name": "buggy_calc", "passed": True},
            {"name": "prompt_injection_repo", "passed": False},
        ],
        context_summary={
            "total_tokens": 1200,
            "cacheable_tokens": 300,
            "dynamic_tokens": 900,
            "large_outputs": [{"name": "noisy_logs", "tokens": 900}],
        },
        policy_violations=[],
    )

    assert "Deployment Recommendation" in report
    assert "human review required" in report.lower()
    assert "prompt_injection_repo" in report
