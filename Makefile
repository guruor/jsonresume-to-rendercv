.PHONY: build test release clean

install:
	pip install -e .[dev]

build:
	python setup.py sdist bdist_wheel

test:
	pytest tests/

release: clean build
	twine upload dist/*

clean:
	rm -rf build dist *.egg-info
