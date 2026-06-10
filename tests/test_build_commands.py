from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_makefile_exposes_html_book_targets() -> None:
    makefile = (ROOT / "Makefile").read_text()

    assert "PYTHON ?= .venv/bin/python" in makefile
    assert ".PHONY: test examples html book check" in makefile
    assert "\ntest:\n\t$(PYTHON) -m pytest\n" in makefile
    assert "\nexamples:\n\t$(PYTHON) scripts/run_all_examples.py\n" in makefile
    assert "\nhtml:\n\tquarto render --to html --no-clean\n" in makefile
    assert "\nbook: html\n" in makefile
    assert "\ncheck: test examples html\n" in makefile
    assert "\npdf:" not in makefile


def test_command_reference_documents_html_book_targets() -> None:
    command_reference = (ROOT / "appendices" / "command-reference.qmd").read_text()
    readme = (ROOT / "README.md").read_text()

    for command in ("make html", "make book", "make check"):
        assert command in command_reference
        assert command in readme

    assert "_book/index.html" in command_reference
    assert "make pdf" not in command_reference
    assert "make pdf" not in readme
    assert "Agentic-Systems-Lab.pdf" not in command_reference
    assert "Agentic-Systems-Lab.pdf" not in readme
    assert "TinyTeX" not in command_reference
    assert "TinyTeX" not in readme


def test_quarto_config_is_html_only() -> None:
    quarto_config = (ROOT / "_quarto.yml").read_text()

    assert "format:\n  html:" in quarto_config
    assert "\n  pdf:" not in quarto_config
    assert "downloads: [pdf]" not in quarto_config
    assert "include-in-header: pdf/code-blocks.tex" not in quarto_config


def test_representative_text_fences_remain_source_blocks() -> None:
    index = (ROOT / "index.qmd").read_text()
    chapter = (ROOT / "chapters" / "01-from-llm-calls-to-agentic-systems.qmd").read_text()
    evidence_policy = (ROOT / "appendices" / "evidence-reference-policy.qmd").read_text()

    assert "```text\nworkflow -> tools -> state -> agent runtime" in index
    assert "```text\nbuild -> tool access -> state/context" in chapter
    assert "```text\nIt is considered best practice to..." in evidence_policy
