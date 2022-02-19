default: dev

.PHONY: dev
dev:
	pip install -e .

.PHONY: upload
upload:
	python setup.py sdist
	twine upload dist/*

.PHONY: test
test:
	pytest
