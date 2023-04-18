ifeq ($(OS),Windows_NT)
    pip := pip
	python := python
else
    pip := pip3
	python := python3
endif

test:
	pytest -vv ./tests

format:
	black ./growtopia
	isort ./growtopia

format-check:
	black --check .
	isort --check-only .

build:
	$(python) setup.py sdist bdist_wheel

install:
	$(pip) install -U .

install2:
	$(pip) install --no-cache-dir --no-dependencies --no-build-isolation -U .