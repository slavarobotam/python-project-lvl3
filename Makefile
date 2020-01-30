.PHONY: install package-install test lint run publish

install:
	@poetry install

pip-install:
	@pip install --user --index-url https://test.pypi.org/simple/ \
		--extra-index-url https://pypi.org/simple/ slavarobotam_page_loader

uninstall:
	@pip uninstall slavarobotam_page_loader

test:
	@poetry run pytest --log-format="%(asctime)s %(levelname)s %(message)s" \
        --log-date-format="%Y-%m-%d %H:%M:%S" -vv --cov=page_loader tests/ --cov-report xml

lint:
	@poetry run flake8 --ignore=F401

publish:
	@poetry build
	@poetry publish -r ott45

test-run:
	@poetry run page-loader -o=TEMP -f=TEMP -l=info https://example.com/
