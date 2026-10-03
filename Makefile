RUFF ?= ruff

.PHONY: generate lint check test verify smoke

generate:
	python3 scripts/catalog.py

lint:
	$(RUFF) check scripts tests
	$(RUFF) format --check scripts tests

check:
	python3 scripts/catalog.py --check
	git diff --check
	claude plugin validate .

test:
	python3 -m unittest discover -s tests -v

verify: lint check test
	python3 scripts/catalog.py --check --remote

smoke:
	python3 scripts/smoke.py
