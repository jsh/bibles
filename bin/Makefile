CHECK := sizes.py gains.py

all: format lint test out.csv

format:
	black -q *.py

lint:
	pylint -rn $(CHECK)
	pylama *.py

test:
	pytest -q --doctest-modules $(CHECK)

out.csv: gains.py
	./gains.py | tee out.csv

.PHONY: format lint test
.SILENT:

