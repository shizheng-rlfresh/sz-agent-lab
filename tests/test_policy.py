from pathlib import Path

import pytest

from agentic_systems_lab.policy import ToolPolicy, ToolPolicyError


def test_policy_allows_paths_inside_allowed_roots(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    file_path = root / "note.md"
    file_path.write_text("ok")

    policy = ToolPolicy(allowed_roots=(root,))

    assert policy.resolve_path(file_path) == file_path.resolve()
    assert policy.violations == []


def test_policy_blocks_path_traversal_and_logs_violation(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    outside = tmp_path / "secret.txt"
    outside.write_text("secret")
    policy = ToolPolicy(allowed_roots=(root,))

    with pytest.raises(ToolPolicyError):
        policy.resolve_path(outside)

    assert len(policy.violations) == 1
    assert policy.violations[0]["reason"] == "path_outside_allowed_roots"


def test_policy_enforces_read_only_and_blocks_shell(tmp_path: Path) -> None:
    policy = ToolPolicy(allowed_roots=(tmp_path,), read_only=True, allow_shell=False)

    with pytest.raises(ToolPolicyError):
        policy.check_write("write_file")
    with pytest.raises(ToolPolicyError):
        policy.check_shell("echo unsafe")

    assert [entry["reason"] for entry in policy.violations] == [
        "write_blocked_read_only",
        "shell_blocked",
    ]


def test_policy_caps_text_output(tmp_path: Path) -> None:
    policy = ToolPolicy(allowed_roots=(tmp_path,), max_file_chars=8)

    capped = policy.cap_text("abcdefghijklmnop", max_chars=12)

    assert capped.startswith("abcdefgh")
    assert "[truncated" in capped
