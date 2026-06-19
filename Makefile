PYTHON ?= .venv/bin/python

.PHONY: preview html clean test examples book check

preview:
	quarto preview

html:
	quarto render --to html --no-clean

clean:
	rm -rf _book .quarto .pytest_cache
	find . -name '*_files' -type d -prune -exec rm -rf {} +

test:
	uv run pytest

examples:
	uv run scripts/run_all_examples.py

book: html

check: test examples html
