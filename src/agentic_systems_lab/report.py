"""Markdown report generation for agent runs."""

from __future__ import annotations

from pathlib import Path

from agentic_systems_lab.context import demo_context_summary
from agentic_systems_lab.evals import run_eval_suite
from agentic_systems_lab.tracer import summarize_trace


def generate_report(
    *,
    trace_path: str | Path | None = None,
    eval_results: list[dict] | None = None,
    context_summary: dict | None = None,
    policy_violations: list[dict] | None = None,
) -> str:
    trace_summary = summarize_trace(trace_path) if trace_path else {}
    eval_results = eval_results or []
    context_summary = context_summary or {}
    policy_violations = policy_violations or []

    lines = [
        "# Agentic Systems Lab Report",
        "",
        "## Trace Summary",
        f"- run_id: {trace_summary.get('run_id')}",
        f"- event_counts: {trace_summary.get('event_counts', {})}",
        f"- tool_calls: {trace_summary.get('tool_calls', 0)}",
        f"- failed_tool_calls: {trace_summary.get('failed_tool_calls', 0)}",
        "",
        "## Eval Results",
    ]
    if eval_results:
        for result in eval_results:
            lines.append(f"- {result.get('name')}: passed={result.get('passed')}")
    else:
        lines.append("- No eval results supplied.")

    lines.extend(["", "## Policy Warnings"])
    if policy_violations:
        for violation in policy_violations:
            lines.append(f"- {violation.get('reason')}: {violation}")
    else:
        lines.append("- No policy violations recorded.")

    lines.extend(
        [
            "",
            "## Context Growth",
            f"- total_tokens: {context_summary.get('total_tokens', 0)}",
            f"- cacheable_tokens: {context_summary.get('cacheable_tokens', 0)}",
            f"- dynamic_tokens: {context_summary.get('dynamic_tokens', 0)}",
        ]
    )
    for output in context_summary.get("large_outputs", []):
        lines.append(f"- large_output: {output.get('name')} tokens={output.get('tokens')}")

    readiness_warnings = []
    if policy_violations:
        readiness_warnings.append("Resolve or explicitly approve policy violations.")
    if context_summary.get("large_outputs"):
        readiness_warnings.append("Add summarization or output caps for large tool observations.")
    if any(not result.get("passed", False) for result in eval_results):
        readiness_warnings.append("Block release until deterministic eval failures are fixed.")
    if not readiness_warnings:
        readiness_warnings.append("Baseline deterministic checks passed; add environment-specific rollout gates.")

    lines.extend(["", "## Production Readiness"])
    lines.extend(f"- {warning}" for warning in readiness_warnings)
    lines.append("")
    return "\n".join(lines)


def write_report(report: str, path: str | Path = "reports/sample_production_report.md") -> Path:
    report_path = Path(path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    return report_path


def main() -> None:
    trace_path = Path("traces/buggy_calc_trace.jsonl")
    eval_results = run_eval_suite()
    report = generate_report(
        trace_path=trace_path if trace_path.exists() else None,
        eval_results=eval_results,
        context_summary=demo_context_summary(),
        policy_violations=[],
    )
    path = write_report(report)
    print(path)


if __name__ == "__main__":
    main()
