ifeq ($(OS),Windows_NT)
    pip := pip
	python := python
else
    pip := pip3
	python := python3
endif

test:
	$(python) -m pytest -vv ./tests

profile:
	$(python) profile_.py

format:
	$(python) -m black ./growtopia ./tests
	$(python) -m isort ./growtopia ./tests

format-check:
	$(python) -m black --check .
	$(python) -m isort --check-only .

build_whl:
	$(python) setup.py sdist bdist_wheel
	$(python) -m build

install:
	$(pip) install -U .

install2:
	rm -r -f build
	rm -r -f growtopia.py.egg-info
	$(pip) install --no-cache-dir --no-dependencies --no-build-isolation -U .

upload:
	make build_whl
	$(python) -m twine upload --repository growtopia.py  dist/*