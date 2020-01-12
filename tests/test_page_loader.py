import pytest  # noqa: F401
import tempfile
import os
from page_loader.engine import _write_to_file, _get_page_source, engine
from page_loader.get_storage_path import get_storage_path
from page_loader.cli import parse_args


def test_get_page_source():
    url = 'https://example.com'
    fixture_path = 'tests/fixtures/expected_text.txt'
    text = _get_page_source(url)
    with open(fixture_path) as fixture:
        expected_result = fixture.read()
        result = text
        assert expected_result == result


def test_engine():
    url = 'https://example.com'
    fixture_path = 'tests/fixtures/expected_page_source.htm'
    with tempfile.TemporaryDirectory() as storage_dir:
        engine(storage_dir, url)
        # open stored file and compare to fixture
        storage_path = os.path.join(storage_dir, 'example-com.html')
        with open(storage_path) as storage:
            with open(fixture_path) as fixture:
                expected_result = fixture.read()
                result = storage.read()
                assert expected_result == result


def test_write_to_file():
    url = 'https://example.com'
    expected_result_path = 'tests/fixtures/expected_text.txt'
    text_fixture = 'tests/fixtures/expected_text.txt'
    # write to file
    with tempfile.TemporaryDirectory() as storage_dir:
        with open(text_fixture) as text_file:
            with open(expected_result_path) as expected:
                expected_result = expected.read()
                text = text_file.read()
                result = _write_to_file(text, storage_dir, url)
    # read from file
        storage_path = get_storage_path(storage_dir, url)
        with open(storage_path) as storage:
            with open(expected_result_path) as expected:
                expected_result = expected.read()
                result = storage.read()
                assert expected_result == result


def test_get_storage_path():
    url = 'https://example.com'
    filename = 'example-com.html'
    with tempfile.TemporaryDirectory() as temp_dir:
        result = get_storage_path(temp_dir, url)
        expected_result = os.path.join(temp_dir, filename)
        assert expected_result == result


def test_parse_args():
    result = parse_args(['-o=dodo', 'https://example.com'])
    expected_result = ('dodo', 'https://example.com')
    assert expected_result == result
