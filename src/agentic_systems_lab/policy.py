"""Tool policy primitives for deterministic agent labs."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


class ToolPolicyError(RuntimeError):
    """Raised when a tool request violates policy."""


def _as_path_tuple(paths: Iterable[str | Path]) -> tuple[Path, ...]:
    return tuple(Path(path).resolve() for path in paths)


@dataclass
class ToolPolicy:
    """Read-only tool policy with explicit path and shell boundaries."""

    allowed_roots: tuple[str | Path, ...] = ("data/toy_repos",)
    read_only: bool = True
    allow_shell: bool = False
    max_file_chars: int = 8000
    approval_required: tuple[str, ...] = ("write_file", "run_shell", "delete_file")
    violations: list[dict] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.allowed_roots = _as_path_tuple(self.allowed_roots)

    def record_violation(self, reason: str, **metadata: object) -> None:
        self.violations.append({"reason": reason, **metadata})

    def resolve_path(self, path: str | Path) -> Path:
        candidate = Path(path).resolve()
        if any(candidate == root or root in candidate.parents for root in self.allowed_roots):
            return candidate
        self.record_violation(
            "path_outside_allowed_roots",
            path=str(path),
            allowed_roots=[str(root) for root in self.allowed_roots],
        )
        raise ToolPolicyError(f"path is outside allowed roots: {path}")

    def check_write(self, action: str) -> None:
        if self.read_only:
            self.record_violation("write_blocked_read_only", action=action)
            raise ToolPolicyError(f"write action blocked by read-only policy: {action}")

    def check_shell(self, command: str) -> None:
        if not self.allow_shell:
            self.record_violation("shell_blocked", action="run_shell", command=command)
            raise ToolPolicyError("shell execution is disabled by policy")

    def cap_text(self, text: str, max_chars: int | None = None) -> str:
        limit = self.max_file_chars
        if max_chars is not None:
            limit = min(limit, max_chars)
        if len(text) <= limit:
            return text
        omitted = len(text) - limit
        return f"{text[:limit]}\n[truncated {omitted} chars]"

    def to_dict(self) -> dict:
        return {
            "allowed_roots": [str(root) for root in self.allowed_roots],
            "read_only": self.read_only,
            "allow_shell": self.allow_shell,
            "max_file_chars": self.max_file_chars,
            "approval_required": list(self.approval_required),
            "violations": list(self.violations),
        }


def main() -> None:
    policy = ToolPolicy()
    print(json.dumps(policy.to_dict(), indent=2))


if __name__ == "__main__":
    main()
