PY := python3


.PHONY: test

test:
	@$(PY) tests/runtests.py
