from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_makefile_exposes_html_book_targets() -> None:
    makefile = (ROOT / "Makefile").read_text()

    assert "PYTHON ?= .venv/bin/python" in makefile
    assert ".PHONY: preview html all clean test examples book check" in makefile
    assert "\npreview:\n\tquarto preview\n" in makefile
    assert "\nhtml:\n\tquarto render --to html --no-clean\n" in makefile
    assert "\nall:\n\tquarto render --to html --no-clean\n" in makefile
    assert "\nclean:\n\trm -rf _book .quarto .pytest_cache\n" in makefile
    assert "\tfind . -name '*_files' -type d -prune -exec rm -rf {} +\n" in makefile
    assert "\ntest:\n\t$(PYTHON) -m pytest\n" in makefile
    assert "\nexamples:\n\t$(PYTHON) scripts/run_all_examples.py\n" in makefile
    assert "\nbook: html\n" in makefile
    assert "\ncheck: test examples html\n" in makefile
    assert "\npdf:" not in makefile
    assert "\nepub:" not in makefile
    assert "\nlatex:" not in makefile


def test_command_reference_documents_html_book_targets() -> None:
    command_reference = (ROOT / "appendices" / "command-reference.qmd").read_text()
    readme = (ROOT / "README.md").read_text()

    for command in ("make preview", "make html", "make all", "make book", "make check", "make clean"):
        assert command in command_reference

    for command in ("uv sync --extra dev", "uv run pytest", "uv run python scripts/run_all_examples.py", "make html"):
        assert command in readme

    assert "python3 -m venv .venv" not in readme
    assert "source .venv/bin/activate" not in readme
    assert 'python -m pip install -e ".[dev]"' not in readme

    assert "_book/index.html" in command_reference
    assert "make pdf" not in command_reference
    assert "make pdf" not in readme
    assert "make epub" not in command_reference
    assert "make epub" not in readme
    assert "make latex" not in command_reference
    assert "make latex" not in readme
    assert "Agentic-Systems-Lab.pdf" not in command_reference
    assert "Agentic-Systems-Lab.pdf" not in readme
    assert "TinyTeX" not in command_reference
    assert "TinyTeX" not in readme


def test_readme_uses_local_book_badge() -> None:
    readme = (ROOT / "README.md").read_text()
    badge = (ROOT / "assets" / "agent-47-badge.svg").read_text()

    assert "[![Agentic Systems Lab badge](assets/agent-47-badge.svg)]" in readme
    assert "https://shizheng-rlfresh.github.io/sz-agent-lab/" in readme
    assert "https://github.com/shizheng-rlfresh/sz-agent-lab/issues" in readme
    assert "https://github.com/shizheng-rlfresh/sz-agent-lab/actions/workflows/book.yml" in readme
    assert "[MIT](LICENSE)" in readme
    assert "[CONTRIBUTING.md](CONTRIBUTING.md)" in readme
    assert "[appendices/command-reference.qmd](appendices/command-reference.qmd)" in readme
    assert "actions/workflows/book.yml/badge.svg" not in readme
    assert "img.shields.io" not in readme
    assert "agent_47_bald_head.png" not in readme
    assert "agent_47_bald_head.png" not in badge
    assert "data:image/png;base64," in badge
    assert "href=\"agent-badge-head.png\"" not in badge
    assert "python -m agentic_systems_lab." not in readme
    assert "make preview" not in readme
    assert "make all" not in readme
    assert "make clean" not in readme
    assert "Hitman" not in badge
    assert ">47<" not in badge
    assert "Agentic Systems Lab" in badge


def test_quarto_config_is_html_only() -> None:
    quarto_config = (ROOT / "_quarto.yml").read_text()

    assert "output-dir: _book" in quarto_config
    assert "format:\n  html:" in quarto_config
    assert "css: styles/html.css" in quarto_config
    assert "\n  pdf:" not in quarto_config
    assert "downloads: [pdf]" not in quarto_config
    assert "include-in-header: pdf/code-blocks.tex" not in quarto_config


def test_adapted_html_template_is_agent_lab_scoped() -> None:
    stylesheet = (ROOT / "styles" / "html.css").read_text()
    template = (ROOT / "templates" / "chapter.qmd").read_text()

    assert "--asl-accent" in stylesheet
    assert ".asl-term" in stylesheet
    assert ".callout.asl-design-rule" in stylesheet
    assert ".callout.asl-production-signal" in stylesheet
    assert "[tool authority]{.asl-term}" in template
    assert "{#def-agentic-system name=\"Agentic system\"}" in template
    assert ".asl-design-rule" in template
    assert ".asl-production-signal" in template
    assert "mlsd" not in stylesheet.lower()
    assert "mlsd" not in template.lower()


def test_representative_text_fences_remain_source_blocks() -> None:
    index = (ROOT / "index.qmd").read_text()
    chapter = (ROOT / "chapters" / "01-from-llm-calls-to-agentic-systems.qmd").read_text()
    evidence_policy = (ROOT / "appendices" / "evidence-reference-policy.qmd").read_text()

    assert "```text\nworkflow -> tools -> state -> agent runtime" in index
    assert "```text\nbuild -> tool access -> state/context" in chapter
    assert "```text\nIt is considered best practice to..." in evidence_policy
