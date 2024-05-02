.PHONY: venv build upload clean veryclean

venv:
	python3 -m venv venv
	. venv/bin/activate
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt

build:
	rm -rf dist
	rm -f pyproject.toml
	python3 ./scripts/generate-pyproject.py
	python3 -m pip install --upgrade build
	python3 -m build

upload:
	python3 -m pip install --upgrade twine
	python3 -m twine upload dist/*

clean:
	rm -rf dist
	rm pyproject.toml

veryclean:
	rm -rf dist
	rm pyproject.toml
	rm -rf venv
