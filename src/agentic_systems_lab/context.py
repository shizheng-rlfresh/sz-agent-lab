"""Context growth and crude cost accounting utilities."""

from __future__ import annotations

import json
import math
import argparse
from dataclasses import dataclass, field


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, math.ceil(len(text) / 4))


STATIC_SEGMENT_NAMES = {"system", "instructions", "tools", "tool_schemas", "schema", "developer"}
DYNAMIC_SEGMENT_NAMES = {"timestamp", "uuid", "user", "task", "retrieval", "tool_result", "memory"}


def _segment_text(segment: dict) -> str:
    return str(segment.get("content", ""))


def _segment_name(segment: dict) -> str:
    return str(segment.get("name", ""))


def analyze_prompt_cache_layouts(baseline: list[dict], candidate: list[dict]) -> dict:
    """Compare prompt segment layouts and identify prefix-cache risk."""

    shared_prefix_tokens = 0
    first_changed_segment = None
    for left, right in zip(baseline, candidate):
        if _segment_name(left) != _segment_name(right) or _segment_text(left) != _segment_text(right):
            first_changed_segment = _segment_name(right) or _segment_name(left)
            break
        shared_prefix_tokens += estimate_tokens(_segment_text(left))

    if first_changed_segment is None and len(candidate) != len(baseline):
        first_changed_segment = _segment_name(candidate[min(len(baseline), len(candidate) - 1)])

    cache_breakers: list[str] = []
    seen_static = False
    for index, segment in enumerate(candidate):
        name = _segment_name(segment).lower()
        if name in STATIC_SEGMENT_NAMES:
            seen_static = True
        if name == "timestamp" and not seen_static:
            cache_breakers.append("timestamp_before_static_prefix")
        if name == "uuid" and not seen_static:
            cache_breakers.append("uuid_before_static_prefix")
        if name in {"retrieval", "tool_result", "memory"} and index < 2:
            cache_breakers.append(f"dynamic_{name}_early")
        if "{" in _segment_text(segment) and "randomized" in name:
            cache_breakers.append("randomized_json_before_static_prefix")

    baseline_tokens = sum(estimate_tokens(_segment_text(segment)) for segment in baseline)
    candidate_tokens = sum(estimate_tokens(_segment_text(segment)) for segment in candidate)
    return {
        "baseline_tokens": baseline_tokens,
        "candidate_tokens": candidate_tokens,
        "shared_prefix_tokens": shared_prefix_tokens,
        "candidate_dynamic_tokens": sum(
            estimate_tokens(_segment_text(segment))
            for segment in candidate
            if _segment_name(segment).lower() in DYNAMIC_SEGMENT_NAMES
        ),
        "first_changed_segment": first_changed_segment,
        "cache_breakers": cache_breakers,
        "recommendations": [
            "Place stable instructions and tool schemas before timestamps, UUIDs, retrieval, memory, and tool output.",
            "Keep JSON serialization deterministic for reusable prompt prefixes.",
            "Treat provider-specific cache behavior as an optimization target, not a correctness dependency.",
        ],
    }


@dataclass
class ContextTracker:
    large_output_token_threshold: int = 1000
    segments: list[dict] = field(default_factory=list)

    def add_segment(self, name: str, content: str, *, cacheable: bool) -> dict:
        tokens = estimate_tokens(content)
        segment = {
            "name": name,
            "chars": len(content),
            "tokens": tokens,
            "cacheable": cacheable,
        }
        self.segments.append(segment)
        return segment

    def summary(self) -> dict:
        total = 0
        steps = []
        for segment in self.segments:
            total += int(segment["tokens"])
            steps.append({**segment, "cumulative_tokens": total})
        cacheable_tokens = sum(int(segment["tokens"]) for segment in self.segments if segment["cacheable"])
        large_outputs = [
            segment
            for segment in self.segments
            if not segment["cacheable"]
            and int(segment["tokens"]) >= self.large_output_token_threshold
        ]
        return {
            "total_tokens": total,
            "cacheable_tokens": cacheable_tokens,
            "dynamic_tokens": total - cacheable_tokens,
            "steps": steps,
            "large_outputs": large_outputs,
            "cacheability_notes": [
                "Stable instructions and tool schemas are cache candidates.",
                "Tool observations and repository contents are dynamic and should appear later.",
            ],
        }


def demo_context_summary() -> dict:
    tracker = ContextTracker(large_output_token_threshold=50)
    tracker.add_segment("system", "stable triage instructions and tool schemas", cacheable=True)
    tracker.add_segment("tool_result", "log line\n" * 80, cacheable=False)
    return tracker.summary()


def cache_demo() -> dict:
    baseline = [
        {"name": "system", "content": "stable instructions"},
        {"name": "tools", "content": json.dumps({"read_file": {"max_chars": 8000}}, sort_keys=True)},
        {"name": "task", "content": "inspect repo"},
    ]
    candidate = [
        {"name": "timestamp", "content": "2026-06-04T12:00:00Z"},
        {"name": "system", "content": "stable instructions"},
        {"name": "tools", "content": json.dumps({"read_file": {"max_chars": 8000}}, sort_keys=True)},
        {"name": "task", "content": "inspect repo"},
    ]
    return analyze_prompt_cache_layouts(baseline, candidate)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-demo", action="store_true")
    args = parser.parse_args()
    payload = cache_demo() if args.cache_demo else demo_context_summary()
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
