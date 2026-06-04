from pathlib import Path

import pytest

from agentic_systems_lab.policy import ToolPolicy, ToolPolicyError
from agentic_systems_lab.tools import grep, list_files, read_file


def test_list_files_is_recursive_sorted_and_relative(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    (root / "b").mkdir(parents=True)
    (root / "a.py").write_text("print('a')\n")
    (root / "b" / "c.py").write_text("print('c')\n")
    policy = ToolPolicy(allowed_roots=(root,))

    assert list_files(root, policy=policy) == ["a.py", "b/c.py"]


def test_read_file_is_capped_by_policy_and_call_limit(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    path = root / "long.txt"
    path.write_text("x" * 32)
    policy = ToolPolicy(allowed_roots=(root,), max_file_chars=12)

    text = read_file(path, max_chars=20, policy=policy)

    assert text.startswith("x" * 12)
    assert "[truncated" in text


def test_grep_returns_structured_deterministic_matches(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "b.py").write_text("alpha\nneedle two\n")
    (root / "a.py").write_text("needle one\nbeta\n")
    policy = ToolPolicy(allowed_roots=(root,))

    assert grep("needle", root, policy=policy) == [
        {"file": "a.py", "line_number": 1, "line": "needle one"},
        {"file": "b.py", "line_number": 2, "line": "needle two"},
    ]


def test_tools_block_paths_outside_policy(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("secret")
    policy = ToolPolicy(allowed_roots=(root,))

    with pytest.raises(ToolPolicyError):
        read_file(outside, policy=policy)
