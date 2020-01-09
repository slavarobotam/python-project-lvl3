install:
	@poetry install

test:
	@poetry run pytest -vv --cov=page_loader tests/ --cov-report xml

lint:
	@poetry run flake8 --ignore=F401

run:
	@poetry run page-loader

.PHONY: install test lint