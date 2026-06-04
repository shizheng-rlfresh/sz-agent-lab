from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_makefile_exposes_format_specific_book_targets() -> None:
    makefile = (ROOT / "Makefile").read_text()

    assert "PYTHON ?= .venv/bin/python" in makefile
    assert ".PHONY: test examples html pdf book check" in makefile
    assert "\ntest:\n\t$(PYTHON) -m pytest\n" in makefile
    assert "\nexamples:\n\t$(PYTHON) scripts/run_all_examples.py\n" in makefile
    assert "\nhtml:\n\tquarto render --to html --no-clean\n" in makefile
    assert "\npdf:\n\tquarto render --to pdf --no-clean\n" in makefile
    assert "\nbook: html pdf\n" in makefile
    assert "\ncheck: test examples book\n" in makefile


def test_command_reference_documents_book_format_targets() -> None:
    command_reference = (ROOT / "appendices" / "command-reference.qmd").read_text()
    readme = (ROOT / "README.md").read_text()

    for command in ("make html", "make pdf", "make book", "make check"):
        assert command in command_reference
        assert command in readme

    assert "_book/index.html" in command_reference
    assert "_book/Agentic-Systems-Lab.pdf" in command_reference
    assert "TinyTeX" in command_reference
