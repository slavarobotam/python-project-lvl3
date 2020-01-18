import pytest  # noqa: F401
import tempfile
import os
import json
import copy
# from page_loader.engine import engine
from page_loader.cli import parse_args
from page_loader.create_path import create_path, make_alphanum
from page_loader.get_data import get_resources_data, get_content
from page_loader.processing import replace_paths, write_to_file


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


# @pytest.mark.skip(reason="works ok")
@pytest.mark.parametrize('url', [
    'https://example.com',
    'http://www.bridgeclub.ru/humor/tsostik1.htm'
])
def test_parse_args(url):
    result = parse_args(['-o=dodo', url])
    expected_result = ('dodo', url)
    assert expected_result == result


# @pytest.mark.skip(reason="works ok")
@pytest.mark.parametrize('url, _type, content_length', [
    ('http://httpbin.org/html', 'text', 3739),
    ('http://httpbin.org/image', 'img', 142)
])
def test_get_content(url, _type, content_length):
    expected_result = content_length
    result = len(get_content(url, _type))
    assert expected_result == result


# @pytest.mark.skip(reason="works ok")
@pytest.mark.parametrize('url, source_data, expected', [
    ('https://test.url/123',
        'tests/fixtures/test_resources_data.html',
        'tests/fixtures/expected_resources_data.json')
])
def test_get_resources_data(url, source_data, expected, open_file, open_json):
    dir_path = '/dir/'
    page_source = open_file(source_data)
    result = get_resources_data(page_source, url, dir_path)
    expected_result = open_json(expected)
    assert expected_result == result


# @pytest.mark.skip(reason="works ok")
@pytest.mark.parametrize('entity_type, url, expected_name', [
    ('page', 'https://example.com', 'example-com.html'),
    ('dir', 'https://xkcd.com/353/', 'xkcd-com-353_files'),
    (None, '2001/IridescentClouds_1500.jpg', '2001-IridescentClouds-1500.jpg')
])
def test_create_path(temp_dir, entity_type, url, expected_name):
    result = create_path(url, temp_dir, entity_type)
    expected_result = os.path.join(temp_dir, expected_name)
    assert expected_result == result


# @pytest.mark.skip(reason="works ok")
@pytest.mark.parametrize('name, expected_name', [
    ('6536?check_point_id=50605', '6536-check-point-id-50605'),
    ('test~test?test$test_test.test', 'test-test-test-test-test-test'),
    ('/query+test:port', '-query-test-port')
])
def test_make_alphanum(name, expected_name):
    result = make_alphanum(name)
    expected_result = expected_name
    assert expected_result == result


# @pytest.mark.skip(reason="works ok")
@pytest.mark.parametrize('page_html, source_json, expected', [
    ('tests/fixtures/test_resources_data.html',
        'tests/fixtures/expected_resources_data.json',
        'tests/fixtures/test_replace_paths.html'),
])
def test_replace_paths(page_html, source_json, expected, open_file, open_json):
    page_source = open_file(page_html)
    source_data = open_json(source_json)
    source_data_copy = copy.deepcopy(source_data)
    result = replace_paths(page_source, source_data_copy)
    expected_result = open_file(expected)
    assert expected_result == result


# @pytest.mark.skip(reason="works ok")
@pytest.mark.parametrize('content_file, write_mode, name', [
    ('tests/fixtures/test_resources_data.html', 'w+', 'o.txt'),
    ('tests/fixtures/cat_in_hat.jpg', 'wb+', 'o.jpg')
])
def test_write_to_file(temp_dir, open_file, content_file, write_mode, name):
    read_mode = 'rb' if write_mode == 'wb+' else 'r'
    content = open_file(content_file, read_mode)
    path = os.path.join(temp_dir, name)
    write_to_file(content, path, write_mode)
    result = open_file(path, read_mode)
    expected_result = content
    assert expected_result == result

# ************************************************************************
# TODO
# @pytest.mark.skip(reason="Need remake")
# def test_download_resources(img_data_set):
#     with tempfile.TemporaryDirectory() as temp_dir:
#         print('dir exists?', os.path.exists(temp_dir))
#         url, name = img_data_set
#         download_img(temp_dir, url)
#         result_path = os.path.join(temp_dir, name)
#         assert os.path.exists(result_path)

# @pytest.mark.skip(reason="Need remake")
# def test_engine(temp_dir, get_file_content, url_data_set):
#     url, name, local_path = url_data_set
#     engine(temp_dir, url)
#     result = get_file_content(os.path.join(temp_dir, name))
#     expected_result = get_file_content(local_path)
#     assert expected_result == result

# ************************************************************************
# @pytest.mark.skip(reason="no way of currently testing this")
# def test_get_path(temp_dir, entity_data_set):
#     url, entity_type, expected_name = entity_data_set
#     result = get_path(temp_dir, url, entity_type)
#     expected_result = os.path.join(temp_dir, expected_name)
#     assert expected_result == result

# @pytest.mark.skip(reason="no way of currently testing this")
# def test_download_img(img_data_set):
#     with tempfile.TemporaryDirectory() as temp_dir:
#         print('dir exists?', os.path.exists(temp_dir))
#         url, name = img_data_set
#         download_img(temp_dir, url)
#         result_path = os.path.join(temp_dir, name)
#         assert os.path.exists(result_path)

# @pytest.mark.skip(reason="no way of currently testing this")
# def test_get_src_list(get_file_content, src_list_data_set):
#     url, src_list, local_path = src_list_data_set
#     page_source = get_file_content(local_path)
#     result = get_src_list(page_source)
#     expected_result = src_list
#     assert expected_result == result
