CHECK := sizes.py gains.py

all: format lint lama pytest out.csv

format:
	black -q *.py

lama:
	pylama *.py

lint:
	pylint -rn $(CHECK)

pytest:
	pytest -q --doctest-modules $(CHECK)

out.csv: gains.py
	./gains.py | tee out.csv

.PHONY: format lama lint pytest
.SILENT:

