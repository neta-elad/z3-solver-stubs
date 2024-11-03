.PHONY: all
all: format type

.PHONY: format
format:
	black src

.PHONY: type
type:
	mypy --strict src

.PHONY: env
env:
	@! [ -d .venv ] && python3.11 -m venv .venv || true
	@echo source .venv/bin/activate

.PHONY: install-dev
install-dev: update-pip
	pip install --force-reinstall -e .[dev]

.PHONY: install
install:
	pip install --force-reinstall .

.PHONY: update-pip
update-pip:
	pip install --upgrade pip

.PHONY: clean
clean:
	rm -r .venv
