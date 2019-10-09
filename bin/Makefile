CHECK := sizes.py gains.py
CORPORA := ot.d nt.d

all: format lint test out.csv

format:
	black -q *.py

lint:
	pylint -rn $(CHECK)
	pylama *.py

test:
	pytest -q --doctest-modules $(CHECK)

out.csv: gains.py $(CORPORA)
	./gains.py | tee out.csv

.PHONY: format lint test
.SILENT:

