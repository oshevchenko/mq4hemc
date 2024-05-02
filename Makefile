.PHONY: venv build upload clean veryclean

VENV_PATH = venv
VENV_BIN_PATH = $(VENV_PATH)/bin


venv:
	python3 -m venv $(VENV_PATH)
	$(VENV_BIN_PATH)/python3 -m pip install --upgrade pip
	$(VENV_BIN_PATH)/python3 -m pip install -r requirements.txt

build:
	rm -rf dist
	rm -f pyproject.toml
	python3 ./scripts/generate-pyproject.py
	python3 -m pip install --upgrade build
	python3 -m build

upload:
	python3 -m pip install --upgrade twine
	python3 -m twine upload --repository testpypi dist/*

clean:
	rm -rf dist
	rm -f pyproject.toml

veryclean:
	rm -rf dist
	rm -f pyproject.toml
	rm -rf $(VENV_PATH)
