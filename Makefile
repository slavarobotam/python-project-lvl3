.PHONY: install package-install test lint run publish

install:
	@poetry install

pip-install:
	@pip install --user --index-url https://test.pypi.org/simple/ \
		--extra-index-url https://pypi.org/simple/ slavarobotam_page_loader

pip-upgrade:
	@pip install --upgrade --user --index-url https://test.pypi.org/simple/ \
		slavarobotam_page_loader

uninstall:
	@pip uninstall slavarobotam_page_loader

test:
	@poetry run pytest -vv --cov=page_loader tests/ --cov-report xml

lint:
	@poetry run flake8 --ignore=F401

publish:
	@poetry build
	@poetry publish -r ott45
