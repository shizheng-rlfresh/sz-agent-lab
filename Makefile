.PHONY: test examples book check

test:
	python -m pytest

examples:
	python scripts/run_all_examples.py

book:
	quarto render

check: test examples book
