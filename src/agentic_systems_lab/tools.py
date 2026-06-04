"""Read-only tools with deterministic output and policy confinement."""

from __future__ import annotations

import json
import re
from pathlib import Path

from agentic_systems_lab.policy import ToolPolicy


def _default_policy() -> ToolPolicy:
    return ToolPolicy()


def _iter_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    return sorted(path for path in root.rglob("*") if path.is_file())


def _relative(path: Path, root: Path) -> str:
    base = root if root.is_dir() else root.parent
    return path.relative_to(base).as_posix()


def list_files(path: str | Path, *, policy: ToolPolicy | None = None) -> list[str]:
    active_policy = policy or _default_policy()
    root = active_policy.resolve_path(path)
    return [_relative(file_path, root) for file_path in _iter_files(root)]


def read_file(
    path: str | Path,
    max_chars: int = 8000,
    *,
    policy: ToolPolicy | None = None,
) -> str:
    active_policy = policy or _default_policy()
    file_path = active_policy.resolve_path(path)
    text = file_path.read_text(encoding="utf-8", errors="replace")
    return active_policy.cap_text(text, max_chars=max_chars)


def grep(pattern: str, path: str | Path, *, policy: ToolPolicy | None = None) -> list[dict]:
    active_policy = policy or _default_policy()
    root = active_policy.resolve_path(path)
    regex = re.compile(pattern)
    matches: list[dict] = []
    for file_path in _iter_files(root):
        text = file_path.read_text(encoding="utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if regex.search(line):
                matches.append(
                    {
                        "file": _relative(file_path, root),
                        "line_number": line_number,
                        "line": line,
                    }
                )
    return matches


def main() -> None:
    root = Path("data/toy_repos/buggy_calc")
    policy = ToolPolicy(allowed_roots=(Path("data/toy_repos"),))
    payload = {
        "root": str(root),
        "files": list_files(root, policy=policy) if root.exists() else [],
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
