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
	@! [ -d .venv ] && python3.11 -m venv .venv || true
	@echo source .venv/bin/activate

.PHONY: install-dev
install-dev: update-pip
	pip install --force-reinstall -e .[test]

.PHONY: install
install:
	pip install --force-reinstall .

.PHONY: update-pip
update-pip:
	pip install --upgrade pip

.PHONY: clean
clean:
	rm -r .venv
