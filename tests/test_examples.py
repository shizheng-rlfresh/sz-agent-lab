from pathlib import Path

from scripts.create_toy_repos import create_toy_repos
from scripts.run_all_examples import run_all_examples


def test_create_toy_repos_and_run_examples(tmp_path: Path) -> None:
    data_root = tmp_path / "toy_repos"
    reports_root = tmp_path / "reports"
    traces_root = tmp_path / "traces"

    create_toy_repos(data_root)
    result = run_all_examples(data_root=data_root, reports_root=reports_root, traces_root=traces_root)

    assert (data_root / "buggy_calc" / "calculator.py").exists()
    assert (data_root / "prompt_injection_repo" / "README.md").exists()
    assert (data_root / "noisy_logs_repo" / "logs.txt").exists()
    assert result["agent"]["findings"]
    assert result["evals"][0]["passed"] is True
    assert (reports_root / "sample_eval_report.md").exists()
    assert (reports_root / "sample_production_report.md").exists()


def test_run_examples_writes_stable_sample_reports(tmp_path: Path) -> None:
    data_root = tmp_path / "toy_repos"
    reports_root = tmp_path / "reports"
    traces_root = tmp_path / "traces"

    run_all_examples(data_root=data_root, reports_root=reports_root, traces_root=traces_root)
    first = {
        path.name: path.read_text()
        for path in sorted(reports_root.glob("sample_*.md"))
    }
    run_all_examples(data_root=data_root, reports_root=reports_root, traces_root=traces_root)
    second = {
        path.name: path.read_text()
        for path in sorted(reports_root.glob("sample_*.md"))
    }

    assert second == first
