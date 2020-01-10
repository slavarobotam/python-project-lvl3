import pytest  # noqa: F401
import tempfile
import os
from page_loader.engine import write_to_file
from page_loader.get_storage_path import get_storage_path


def test_loading_page():
    url = 'https://slavarobotam.github.io/'
    fixture_path = 'tests/fixtures/expected_loading_page.htm'
    with tempfile.TemporaryDirectory() as dir:
        storage_path = get_storage_path(dir, url)
        write_to_file(url, storage_path)
        with open(storage_path) as storage:
            with open(fixture_path) as fixture:
                expected_result = fixture.read()
                result = storage.read()
                assert expected_result == result


def test_write_to_file():
    url = 'https://slavarobotam.github.io/'
    fixture_path = 'tests/fixtures/expected_write_to_file.txt'
    with tempfile.TemporaryDirectory() as dir:
        filename = 'slavarobotam-github-io.html'
        storage_path = os.path.join(dir, filename)
        write_to_file(url, storage_path)
        with open(storage_path) as storage:
            with open(fixture_path) as fixture:
                expected_result = fixture.read()
                result = storage.read()
                assert expected_result == result


def test_get_storage_path():
    url = 'https://slavarobotam.github.io/'
    filename = 'slavarobotam-github-io.html'
    with tempfile.TemporaryDirectory() as dir:
        result = get_storage_path(dir, url)
        expected_result = os.path.join(dir, filename)
        assert expected_result == result
