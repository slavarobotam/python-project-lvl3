import copy
import json
import os
import tempfile
from stat import S_IREAD, S_IRGRP, S_IROTH

import pytest  # noqa: F401
import requests

from page_loader.cli import parse_args
from page_loader.engine import run_engine
from page_loader.fetching import ensure_scheme, fetch_data, get_response
from page_loader.logging import run_logging
from page_loader.path import create_path, make_alphanum
from page_loader.processing import (download, get_resources_data, make_paths,
                                    process_data, replace_paths)
from page_loader.storing import write_to_file


@pytest.fixture
def tempdir():
    with tempfile.TemporaryDirectory() as storage_dir:
        yield storage_dir


@pytest.fixture
def open_json():
    def open_path(path):
        with open(path) as file_object:
            return json.load(file_object)
    return open_path


@pytest.fixture
def open_file():
    def open_path(path, mode='r'):
        with open(path, mode) as file_object:
            return file_object.read()
    return open_path


def test_parse_args():
    argv = '-o=test_dir -l=debug http://test.com'.split()
    args = parse_args(argv)
    assert args.url == 'http://test.com'
    assert args.output == 'test_dir'
    assert args.level == 'debug'


@pytest.mark.parametrize('url, expected_result', [
    ('https://ya.ru', 'https://ya.ru'),
    ('ya.ru', 'http://ya.ru')])
def test_ensure_scheme(url, expected_result):
    result = ensure_scheme(url)
    assert expected_result == result


def test_fetch_data():
    url = 'example.com'

    def mock_getresponse(url):
        response = 'response'
        return response

    def mock_getcontent(response):
        source = 'page_source'
        return source
    result = fetch_data(url, mock_getresponse, mock_getcontent)
    expected_result = ('page_source', 'http://example.com')
    assert expected_result == result


@pytest.mark.parametrize('url, source, expected', [
    ('https://test.url/123',
        'tests/fixtures/page_source.html',
        'tests/fixtures/resources_data.json')])
def test_get_resources_data(url, source, expected, open_file, open_json):
    dir_path = '/testdir/test-url-123_files/'
    page_source = open_file(source)
    resources_data = get_resources_data(page_source, url)
    result = make_paths(resources_data, url, dir_path)
    expected_result = open_json(expected)
    assert expected_result == result


def test_make_paths(open_json):
    resources_data = open_json('tests/fixtures/resources_no_paths.json')
    url = 'https://test.url'
    dir_path = '/testdir/test-url-123_files'
    result = make_paths(resources_data, url, dir_path)
    expected_result = open_json('tests/fixtures/resources_data.json')
    assert expected_result == result


@pytest.mark.parametrize('entity_type, url, expected_name', [
    ('page', 'https://example.com', 'example-com.html'),
    ('dir', 'https://xkcd.com/353/', 'xkcd-com-353_files'),
    (None, '2001/IridClouds_1500.jpg', '2001-IridClouds-1500.jpg')])
def test_create_path(tempdir, entity_type, url, expected_name):
    result = create_path(url, tempdir, entity_type)
    expected_result = os.path.join(tempdir, expected_name)
    assert expected_result == result


@pytest.mark.parametrize('entity_type, url, expected_name', [
    ('page', 'https://example.com', 'example-com.html'),
    ('dir', 'https://xkcd.com/353/', 'xkcd-com-353_files'),
    (None, '2001/IridClouds_1500.jpg', '2001-IridClouds-1500.jpg')])
def test_create_path_none_dir(monkeypatch, tempdir, entity_type, url,
                              expected_name):
    def mock_getcwd():
        return tempdir
    monkeypatch.setattr(os, 'getcwd', mock_getcwd)
    result = create_path(url, None, entity_type)
    expected_result = os.path.join(tempdir, expected_name)
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


def test_process_data(open_file):
    page_source = open_file('tests/fixtures/page_source.html')
    url = 'https://test.url/123'
    storage_dir = 'testdir'

    def mock_download(*args):
        return 'Downloaded'

    def mock_createpath(*args, **kwargs):
        return '/testdir/test-url-123_files/'

    result = process_data(page_source, url, storage_dir, mock_download,
                          mock_createpath)
    expected_result = open_file('tests/fixtures/local_source.html')
    assert expected_result == result


@pytest.mark.parametrize('_file, write_mode, name', [
    ('tests/fixtures/page_source.html', 'w+', 'o.txt'),
    ('tests/fixtures/cat_in_hat.jpg', 'wb+', 'o.jpg')])
def test_save(_file, write_mode, name, tempdir, open_file):
    read_mode = 'rb' if write_mode == 'wb+' else 'r'
    content = open_file(_file, read_mode)

    path = os.path.join(tempdir, name)
    write_to_file(content, path, write_mode)

    result = open_file(path, read_mode)
    expected_result = content
    assert expected_result == result


@pytest.mark.parametrize('json, expected', [
    ('tests/fixtures/resources_data.json',
        {
            '/testdir/test-url-123_files/test-url-s-link.css',
            '/testdir/test-url-123_files/test-url-s-script.js',
            '/testdir/test-url-123_files/test-url-s-img.png'})])
def test_download_resources(open_json, json, expected):
    resources_data = open_json(json)
    written_files = set()
    dire_path = '/testdir/test-url-123_files/'

    def mock_getresponse(url, _type):
        return url

    def mock_getcontent(response, _type):
        return response

    def mock_save(content, local_path, writing_mode):
        written_files.add(local_path)
    download(resources_data, dire_path, mock_getresponse, mock_getcontent,
             mock_save, need_dir=False)
    result = {v['local_path'] for v in resources_data.values()}
    assert expected == result


def test_run_logging(tempdir, caplog):
    run_logging(level='debug', filepath=tempdir)
    assert 'Logging works fine' in caplog.text


def test_run_logging_error(tempdir):
    os.chmod(tempdir, S_IREAD | S_IRGRP | S_IROTH)
    with pytest.raises(PermissionError) as exc_info:
        level = 'info'
        filepath = os.path.join(tempdir, 'debug.log')
        run_logging(level, filepath)
    assert 'PermissionError' in exc_info.exconly()


def test_error_wrong_url():
    url = 'https://wrong_url'
    with pytest.raises(requests.exceptions.RequestException) as exc_info:
        get_response(url)
    assert 'requests.exceptions' in exc_info.exconly()


def test_error_no_directory():
    content = 'some content'
    storage_path = '/nonexistent-directory/file'
    with pytest.raises(FileNotFoundError) as exc_info:
        write_to_file(content, storage_path, 'w')
    assert 'FileNotFoundError' in exc_info.exconly()


@pytest.mark.parametrize('url, expected_result', [
    ('http://example.com', True),
    ('http://wrong_url', False)])
def test_engine(url, expected_result):
    args = parse_args([url])
    result = run_engine(args)
    assert expected_result == result
