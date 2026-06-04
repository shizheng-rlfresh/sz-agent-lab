"""Markdown report generation for agent runs."""

from __future__ import annotations

from pathlib import Path

from agentic_systems_lab.context import ContextTracker
from agentic_systems_lab.agent import run_repo_triage
from agentic_systems_lab.evals import EvalTask, default_tasks, evaluate_result, write_eval_report
from agentic_systems_lab.policy import ToolPolicy
from agentic_systems_lab.tools import list_files, read_file
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
    failed = [result.get("name") for result in eval_results if not result.get("passed", False)]
    if failed or policy_violations or context_summary.get("large_outputs"):
        recommendation = "human review required before deployment"
    else:
        recommendation = "baseline deterministic gate passed"
    lines.extend(
        [
            "",
            "## Deployment Recommendation",
            f"- status: {recommendation}",
        ]
    )
    if failed:
        lines.append(f"- failed_evals: {', '.join(str(name) for name in failed)}")
    lines.append("")
    return "\n".join(lines)


def write_report(report: str, path: str | Path = "reports/sample_production_report.md") -> Path:
    report_path = Path(path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    return report_path


def _sample_context_summary(data_root: Path) -> dict:
    tracker = ContextTracker(large_output_token_threshold=200)
    tracker.add_segment("system", "stable triage instructions and tool schemas", cacheable=True)
    tracker.add_segment(
        "noisy_logs",
        read_file(data_root / "noisy_logs_repo" / "logs.txt", max_chars=2400, policy=ToolPolicy(allowed_roots=(data_root,))),
        cacheable=False,
    )
    return tracker.summary()


def _sample_eval_results(data_root: Path, traces_root: Path) -> list[dict]:
    results: list[dict] = []
    for task in default_tasks():
        repo_path = data_root / Path(task.repo_path).name
        policy = ToolPolicy(allowed_roots=(data_root,))
        agent_result = run_repo_triage(
            repo_path,
            trace_path=traces_root / f"{task.name}_report_eval_trace.jsonl",
            run_id=f"run_{task.name}_report_eval_sample",
            policy=policy,
        )
        rooted_task = EvalTask(
            name=task.name,
            repo_path=str(repo_path),
            expected_file=task.expected_file,
            expected_keyword=task.expected_keyword,
            allowed_files=tuple(list_files(repo_path, policy=policy)),
        )
        results.append(
            evaluate_result(rooted_task, agent_result, invalid_tool_call_count=len(policy.violations))
        )
    return results


def main() -> None:
    trace_path = Path("traces/buggy_calc_trace.jsonl")
    data_root = Path("data/toy_repos")
    repo_path = Path("data/toy_repos/buggy_calc")
    policy = ToolPolicy(allowed_roots=(data_root,))
    agent_result = run_repo_triage(
        repo_path,
        trace_path=trace_path,
        run_id="run_buggy_calc_sample",
        policy=policy,
    )
    task = EvalTask(
        name="buggy_calc",
        repo_path=str(repo_path),
        expected_file="calculator.py",
        expected_keyword="division",
        allowed_files=tuple(list_files(repo_path, policy=policy)),
    )
    eval_results = _sample_eval_results(data_root, Path("traces"))
    eval_results[0] = evaluate_result(task, agent_result, invalid_tool_call_count=len(policy.violations))
    write_eval_report(eval_results, "reports/sample_eval_report.md")
    report = generate_report(
        trace_path=trace_path,
        eval_results=eval_results,
        context_summary=_sample_context_summary(data_root),
        policy_violations=policy.violations,
    )
    path = write_report(report)
    print(path)


if __name__ == "__main__":
    main()
