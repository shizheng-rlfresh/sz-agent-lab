import json
from pathlib import Path

from agentic_systems_lab.tracer import TraceLogger, summarize_trace


def test_trace_logger_writes_jsonl_events_with_run_id(tmp_path: Path) -> None:
    trace_path = tmp_path / "trace.jsonl"
    logger = TraceLogger(trace_path, run_id="run_test")

    logger.log_event("agent_start", goal="triage")
    logger.log_event("tool_call", tool="read_file", success=True, latency_ms=3)

    events = [json.loads(line) for line in trace_path.read_text().splitlines()]
    assert [event["type"] for event in events] == ["agent_start", "tool_call"]
    assert {event["run_id"] for event in events} == {"run_test"}


def test_summarize_trace_counts_events_and_tool_calls(tmp_path: Path) -> None:
    trace_path = tmp_path / "trace.jsonl"
    logger = TraceLogger(trace_path, run_id="run_test")
    logger.log_event("agent_start")
    logger.log_event("tool_call", tool="list_files", success=True, latency_ms=1)
    logger.log_event("tool_call", tool="read_file", success=False, latency_ms=2)

    summary = summarize_trace(trace_path)

    assert summary["event_counts"] == {"agent_start": 1, "tool_call": 2}
    assert summary["tool_calls"] == 2
    assert summary["failed_tool_calls"] == 1


def test_trace_logger_starts_new_file_for_repeatable_runs(tmp_path: Path) -> None:
    trace_path = tmp_path / "trace.jsonl"
    first = TraceLogger(trace_path, run_id="run_first")
    first.log_event("agent_start")

    second = TraceLogger(trace_path, run_id="run_second")
    second.log_event("agent_start")

    events = [json.loads(line) for line in trace_path.read_text().splitlines()]
    assert len(events) == 1
    assert events[0]["run_id"] == "run_second"
