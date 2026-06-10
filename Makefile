PYTHON ?= .venv/bin/python

.PHONY: test examples html book check

test:
	$(PYTHON) -m pytest

examples:
	$(PYTHON) scripts/run_all_examples.py

html:
	quarto render --to html --no-clean

book: html

check: test examples html
