ifeq ($(OS),Windows_NT)
    pip := pip
	python := python
else
    pip := pip3
	python := python3
endif

test:
	$(python) -m pytest -vv ./tests

format:
	$(python) -m black ./growtopia
	$(python) -m isort ./growtopia

format-check:
	$(python) -m black --check .
	$(python) -m isort --check-only .

_build:
	$(python) setup.py sdist bdist_wheel
	$(python) -m build

install:
	$(pip) install -U .

install2:
	$(pip) install --no-cache-dir --no-dependencies --no-build-isolation -U .

upload:
	make _build
	$(python) -m twine upload --repository growtopia.py  dist/*