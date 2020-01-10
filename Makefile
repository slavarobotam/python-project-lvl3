install:
	@poetry install

test:
	@poetry run pytest -vv --cov=page_loader tests/ --cov-report xml

lint:
	@poetry run flake8 --ignore=F401

run:
	@poetry run page-loader https://slavarobotam.github.io/

publish:
	@poetry build
	@poetry publish -r ott45
.PHONY: install test lint