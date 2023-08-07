.PHONY: all
all: format type

.PHONY: format
format:
	black .

.PHONY: type
type:
	mypy --strict z3-stubs

.PHONY: env
env:
	! [ -d .venv ] && python3 -m venv .venv || true

.PHONY: install
install:
	yes | pip uninstall z3-solver-stubs
	pip install -e .[test]

.PHONY: clean
clean:
	rm -r .venv
