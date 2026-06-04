import json
import subprocess
import sys

from agentic_systems_lab.context import (
    ContextTracker,
    analyze_prompt_cache_layouts,
    estimate_tokens,
)


def test_estimate_tokens_is_deterministic_and_nonzero_for_text() -> None:
    assert estimate_tokens("") == 0
    assert estimate_tokens("abcd") == 1
    assert estimate_tokens("abcde") == 2


def test_context_tracker_reports_growth_large_outputs_and_cacheability() -> None:
    tracker = ContextTracker(large_output_token_threshold=3)
    tracker.add_segment("system", "stable instructions", cacheable=True)
    tracker.add_segment("tool", "x" * 20, cacheable=False)

    summary = tracker.summary()

    assert summary["total_tokens"] == estimate_tokens("stable instructions") + 5
    assert summary["cacheable_tokens"] == estimate_tokens("stable instructions")
    assert summary["dynamic_tokens"] == 5
    assert summary["large_outputs"][0]["name"] == "tool"
    assert [step["cumulative_tokens"] for step in summary["steps"]] == [
        estimate_tokens("stable instructions"),
        summary["total_tokens"],
    ]


def test_prompt_cache_layout_analysis_finds_first_changed_segment_and_breakers() -> None:
    baseline = [
        {"name": "system", "content": "stable instructions"},
        {"name": "tools", "content": '{"read_file": "schema"}'},
        {"name": "task", "content": "inspect repo"},
    ]
    candidate = [
        {"name": "timestamp", "content": "2026-06-04T12:00:00Z"},
        {"name": "system", "content": "stable instructions"},
        {"name": "tools", "content": '{"read_file": "schema"}'},
        {"name": "task", "content": "inspect repo"},
    ]

    analysis = analyze_prompt_cache_layouts(baseline, candidate)

    assert analysis["first_changed_segment"] == "timestamp"
    assert analysis["shared_prefix_tokens"] == 0
    assert "timestamp_before_static_prefix" in analysis["cache_breakers"]
    assert analysis["recommendations"]


def test_context_cache_demo_cli_outputs_json() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "agentic_systems_lab.context", "--cache-demo"],
        check=True,
        text=True,
        capture_output=True,
    )

    payload = json.loads(completed.stdout)
    assert payload["first_changed_segment"] == "timestamp"
    assert "timestamp_before_static_prefix" in payload["cache_breakers"]
