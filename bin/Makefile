.SILENT:

CHECK := sizes.py

all: format lint lama pytest

format:
	black -q *.py

lama:
	pylama *.py

lint:
	pylint -rn $(CHECK)

pytest:
	pytest -q --doctest-modules $(CHECK)

.PHONY: format lama lint pytest
