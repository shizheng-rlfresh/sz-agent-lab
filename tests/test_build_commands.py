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


def test_pdf_code_block_header_overrides_shaded_width() -> None:
    quarto_config = (ROOT / "_quarto.yml").read_text()
    header = ROOT / "pdf" / "code-blocks.tex"

    assert "include-in-header: pdf/code-blocks.tex" in quarto_config
    assert header.exists()

    header_text = header.read_text()
    assert r"\renewenvironment{Shaded}" in header_text
    assert r"\begin{shaded}" in header_text
    assert r"\begin{snugshade}" not in header_text


def test_representative_text_fences_remain_source_blocks() -> None:
    index = (ROOT / "index.qmd").read_text()
    chapter = (ROOT / "chapters" / "01-from-llm-calls-to-agentic-systems.qmd").read_text()
    evidence_policy = (ROOT / "appendices" / "evidence-reference-policy.qmd").read_text()

    assert "```text\nworkflow -> tools -> state -> agent runtime" in index
    assert "```text\nbuild -> tool access -> state/context" in chapter
    assert "```text\nIt is considered best practice to..." in evidence_policy
