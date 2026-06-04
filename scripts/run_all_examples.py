"""Run the deterministic lab examples end to end."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from agentic_systems_lab.agent import run_repo_triage
from agentic_systems_lab.context import ContextTracker
from agentic_systems_lab.evals import EvalTask, evaluate_result, write_eval_report
from agentic_systems_lab.policy import ToolPolicy
from agentic_systems_lab.report import generate_report, write_report
from agentic_systems_lab.tools import grep, list_files, read_file
from agentic_systems_lab.tracer import summarize_trace
try:
    from scripts.create_toy_repos import create_toy_repos
except ModuleNotFoundError:
    from create_toy_repos import create_toy_repos


def _context_for_noisy_repo(data_root: Path) -> dict:
    policy = ToolPolicy(allowed_roots=(data_root,))
    tracker = ContextTracker(large_output_token_threshold=200)
    tracker.add_segment("system", "stable triage instructions and tool schemas", cacheable=True)
    tracker.add_segment(
        "noisy_logs",
        read_file(data_root / "noisy_logs_repo" / "logs.txt", max_chars=2400, policy=policy),
        cacheable=False,
    )
    return tracker.summary()


def run_workflow_baseline(data_root: Path) -> dict:
    policy = ToolPolicy(allowed_roots=(data_root,))
    repo = data_root / "buggy_calc"
    return {
        "files": list_files(repo, policy=policy),
        "division_mentions": grep("divide|division", repo, policy=policy),
    }


def run_all_examples(
    *,
    data_root: str | Path = "data/toy_repos",
    reports_root: str | Path = "reports",
    traces_root: str | Path = "traces",
    example: str = "all",
) -> dict:
    data_root = create_toy_repos(data_root)
    reports_root = Path(reports_root)
    traces_root = Path(traces_root)
    reports_root.mkdir(parents=True, exist_ok=True)
    traces_root.mkdir(parents=True, exist_ok=True)

    payload: dict[str, object] = {}
    if example in {"all", "workflow_baseline"}:
        payload["workflow_baseline"] = run_workflow_baseline(data_root)

    if example in {"all", "repo_triage_agent"}:
        trace_path = traces_root / "buggy_calc_trace.jsonl"
        policy = ToolPolicy(allowed_roots=(data_root,))
        agent_result = run_repo_triage(data_root / "buggy_calc", trace_path=trace_path, policy=policy)
        payload["agent"] = agent_result
        payload["trace"] = summarize_trace(trace_path)
        task = EvalTask(
            name="buggy_calc",
            repo_path=str(data_root / "buggy_calc"),
            expected_file="calculator.py",
            expected_keyword="division",
            allowed_files=tuple(list_files(data_root / "buggy_calc", policy=policy)),
        )
        eval_results = [evaluate_result(task, agent_result, invalid_tool_call_count=len(policy.violations))]
        write_eval_report(eval_results, reports_root / "sample_eval_report.md")
        payload["evals"] = eval_results
        context_summary = _context_for_noisy_repo(data_root)
        payload["context"] = context_summary
        report = generate_report(
            trace_path=trace_path,
            eval_results=eval_results,
            context_summary=context_summary,
            policy_violations=policy.violations,
        )
        write_report(report, reports_root / "sample_production_report.md")
        (reports_root / "sample_trace_report.md").write_text(
            "# Trace Report\n\n"
            f"```json\n{json.dumps(payload['trace'], indent=2)}\n```\n",
            encoding="utf-8",
        )

    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--example",
        choices=["all", "workflow_baseline", "repo_triage_agent"],
        default="all",
    )
    args = parser.parse_args()
    print(json.dumps(run_all_examples(example=args.example), indent=2))


if __name__ == "__main__":
    main()
