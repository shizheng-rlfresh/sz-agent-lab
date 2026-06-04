"""Context growth and crude cost accounting utilities."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, math.ceil(len(text) / 4))


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


def main() -> None:
    print(json.dumps(demo_context_summary(), indent=2))


if __name__ == "__main__":
    main()
