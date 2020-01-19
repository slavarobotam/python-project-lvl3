import pytest  # noqa: F401
import tempfile
import os
import json
import copy
from page_loader.cli import parse_args
from page_loader.create_path import create_path, make_alphanum
from page_loader.get_data import get_resources_data, get_content
from page_loader.processing import (replace_paths, write_to_file,
                                    download_resources)


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as storage_dir:
        return storage_dir


@pytest.fixture
def open_json():
    def get_content(path):
        with open(path) as filename:
            return json.load(filename)
    return get_content


@pytest.fixture
def open_file():
    def get_content(path, mode='r'):
        with open(path, mode) as filename:
            return filename.read()
    return get_content


@pytest.mark.parametrize('argv, expected_result', [
    (['http://test.com', '-o=test_dir'], ('test_dir', 'http://test.com')),
    (['http://test.com'],
        ('/Users/mari/hexlet/python-project-lvl3', 'http://test.com'))])
def test_parse_args(argv, expected_result):
    result = parse_args(argv)
    assert expected_result == result


@pytest.mark.parametrize('url, _type, content_length', [
    ('http://httpbin.org/html', 'text', 3739),
    ('http://httpbin.org/image', 'img', 142)])
def test_get_content(url, _type, content_length):
    expected_result = content_length
    result = len(get_content(url, _type))
    assert expected_result == result


@pytest.mark.parametrize('url, source, expected', [
    ('https://test.url/123',
        'tests/fixtures/page_source.html',
        'tests/fixtures/resources_data.json')])
def test_get_resources_data(url, source, expected, open_file, open_json):
    dir_path = '/dir/'
    page_source = open_file(source)
    result = get_resources_data(page_source, url, dir_path)
    expected_result = open_json(expected)
    assert expected_result == result


@pytest.mark.parametrize('entity_type, url, expected_name', [
    ('page', 'https://example.com', 'example-com.html'),
    ('dir', 'https://xkcd.com/353/', 'xkcd-com-353_files'),
    (None, '2001/IridClouds_1500.jpg', '2001-IridClouds-1500.jpg')])
def test_create_path(temp_dir, entity_type, url, expected_name):
    result = create_path(url, temp_dir, entity_type)
    expected_result = os.path.join(temp_dir, expected_name)
    assert expected_result == result


@pytest.mark.parametrize('name, expected_name', [
    ('test~test?t$e_s.tid=5', 'test-test-t-e-s-tid-5'),
    ('/query+test:port', '-query-test-port')])
def test_make_alphanum(name, expected_name):
    result = make_alphanum(name)
    expected_result = expected_name
    assert expected_result == result


@pytest.mark.parametrize('page, resources, expected', [
    ('tests/fixtures/page_source.html',
        'tests/fixtures/resources_data.json',
        'tests/fixtures/local_source.html')])
def test_replace_paths(page, resources, expected, open_file, open_json):
    page_source = open_file(page)
    resources_data = open_json(resources)
    resources_data_copy = copy.deepcopy(resources_data)
    result = replace_paths(page_source, resources_data_copy)
    expected_result = open_file(expected)
    assert expected_result == result


@pytest.mark.parametrize('_file, write_mode, name', [
    ('tests/fixtures/page_source.html', 'w+', 'o.txt'),
    ('tests/fixtures/cat_in_hat.jpg', 'wb+', 'o.jpg')])
def test_write_to_file(_file, write_mode, name, temp_dir, open_file):
    read_mode = 'rb' if write_mode == 'wb+' else 'r'
    content = open_file(_file, read_mode)

    path = os.path.join(temp_dir, name)
    write_to_file(content, path, write_mode)

    result = open_file(path, read_mode)
    expected_result = content
    assert expected_result == result


@pytest.mark.parametrize('resourses, expected_result', [
    ('tests/fixtures/resources_data.json',
        {
            '/dir/test-url-s-link.css',
            '/dir/test-url-s-script.js',
            '/dir/test-url-s-img.png'})])
def test_download_resources(open_json, resourses, expected_result):
    resources_data = open_json(resourses)
    written_files = set()

    def mock_getcontent(url, _type):
        return url

    def mock_write(content, local_path, writing_mode):
        written_files.add(local_path)
    download_resources(resources_data, mock_getcontent, mock_write)
    result = {v['local_path'] for v in resources_data.values()}
    assert expected_result == result
