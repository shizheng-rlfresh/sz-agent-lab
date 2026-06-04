PYTHON ?= .venv/bin/python

.PHONY: test examples html pdf book check

test:
	$(PYTHON) -m pytest

examples:
	$(PYTHON) scripts/run_all_examples.py

html:
	quarto render --to html --no-clean

pdf:
	quarto render --to pdf --no-clean

book: html pdf

check: test examples book
