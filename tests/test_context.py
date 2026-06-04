from agentic_systems_lab.context import ContextTracker, estimate_tokens


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
