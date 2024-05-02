.PHONY: venv build upload clean veryclean test

VENV_PATH = venv
VENV_BIN_PATH = $(VENV_PATH)/bin

venv:
	python3 -m venv $(VENV_PATH)
	$(VENV_BIN_PATH)/python3 -m pip install --upgrade pip
	$(VENV_BIN_PATH)/python3 -m pip install -r requirements.txt
	$(VENV_BIN_PATH)/python3 -m pip install --upgrade build
	$(VENV_BIN_PATH)/python3 -m pip install --upgrade twine

build:
	rm -rf dist
	rm -f pyproject.toml
	$(VENV_BIN_PATH)/python3 ./scripts/generate-pyproject.py
	$(VENV_BIN_PATH)/python3 -m build

upload:
	$(VENV_BIN_PATH)/python3 -m twine upload --repository testpypi dist/*

clean:
	rm -rf dist
	rm -f pyproject.toml

veryclean:
	rm -rf dist
	rm -f pyproject.toml
	rm -rf $(VENV_PATH)

test:
	$(VENV_BIN_PATH)/python3 -m unittest discover -s tests

install:
	$(VENV_BIN_PATH)/python3 -m pip install --force-reinstall dist/*.whl
