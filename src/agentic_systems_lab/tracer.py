"""JSONL tracing for deterministic agent runs."""

from __future__ import annotations

import json
import time
from collections import Counter
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4


REQUIRED_EVENT_TYPES = {
    "agent_start",
    "tool_call",
    "context_observation",
    "policy_check",
    "eval_check",
    "agent_finish",
}


def new_run_id() -> str:
    return f"run_{uuid4().hex[:12]}"


@dataclass
class TraceLogger:
    path: str | Path
    run_id: str = field(default_factory=new_run_id)

    def __post_init__(self) -> None:
        self.path = Path(self.path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log_event(self, event_type: str, **fields: object) -> dict:
        if event_type not in REQUIRED_EVENT_TYPES:
            raise ValueError(f"unknown trace event type: {event_type}")
        event = {
            "run_id": self.run_id,
            "type": event_type,
            "timestamp": datetime.now(UTC).isoformat(),
            **fields,
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, sort_keys=True) + "\n")
        return event

    def timed_tool_call(self, tool: str, func, **fields: object):
        start = time.perf_counter()
        success = False
        try:
            result = func()
            success = True
            return result
        finally:
            latency_ms = round((time.perf_counter() - start) * 1000, 3)
            self.log_event(
                "tool_call",
                tool=tool,
                success=success,
                latency_ms=latency_ms,
                **fields,
            )


def load_trace(path: str | Path) -> list[dict]:
    trace_path = Path(path)
    if not trace_path.exists():
        return []
    return [json.loads(line) for line in trace_path.read_text().splitlines() if line.strip()]


def summarize_trace(path: str | Path) -> dict:
    events = load_trace(path)
    event_counts = Counter(event["type"] for event in events)
    tool_events = [event for event in events if event["type"] == "tool_call"]
    return {
        "path": str(path),
        "run_id": events[0]["run_id"] if events else None,
        "event_counts": dict(event_counts),
        "tool_calls": len(tool_events),
        "failed_tool_calls": sum(1 for event in tool_events if not event.get("success", False)),
        "total_latency_ms": round(
            sum(float(event.get("latency_ms", 0)) for event in tool_events), 3
        ),
    }


def main() -> None:
    path = Path("traces/demo_trace.jsonl")
    logger = TraceLogger(path, run_id="run_demo")
    logger.log_event("agent_start", goal="demo")
    logger.log_event("agent_finish", success=True)
    print(json.dumps(summarize_trace(path), indent=2))


if __name__ == "__main__":
    main()
