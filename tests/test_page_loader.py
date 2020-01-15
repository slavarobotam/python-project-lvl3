import pytest  # noqa: F401
import tempfile
import os
from page_loader.engine import _write_to_file, _get_page_source, engine, \
    download_img, get_src_list
from page_loader.get_storage_path import get_storage_path
from page_loader.cli import parse_args


ENTITY_DATA_SETS = [
    {
        'type': 'page',
        'url': 'https://example.com',
        'expected_name': 'example-com.html'},
    {
        'type': 'dir',
        'url': 'https://xkcd.com/353/',
        'expected_name': 'xkcd-com-353_files'},
    {
        'type': None,
        'url': 'image/2001/IridescentClouds_Strand_1500.jpg',
        'expected_name': 'image-2001-IridescentClouds-Strand-1500.jpg'}
]

URL_DATA_SETS = [
    {
        'url': 'https://example.com',
        'name': 'example-com.html',
        'local_path': 'tests/fixtures/expected_example_com.htm'},
    {
        'url': 'https://xkcd.com/353/',
        'name': 'xkcd-com-353.html',
        'local_path': 'tests/fixtures/expected_xkcd_com.html'}
]

IMG_DATA_SETS = [
    {
        'url': 'http://www.bridgeclub.ru/im/bal.jpg',
        'name': 'www-bridgeclub-ru-im-bal.jpg'}
]

SRC_LIST_DATA_SET = [
    {
        'url': 'http://www.bridgeclub.ru/humor/tsostik1.htm',
        'local_path': 'tests/fixtures/expected_src_list.html',
        'src_list': [
            '../logo.gif', '../yl_u.gif', '../im/old.jpg',
            '../yl_u.gif', '../yl_b.gif']
    }
]


@pytest.fixture(params=ENTITY_DATA_SETS)
def entity_data_set(request):
    url = request.param['url']
    entity_type = request.param['type']
    expected_name = request.param['expected_name']
    return url, entity_type, expected_name


@pytest.fixture(params=URL_DATA_SETS)
def url_data_set(request):
    url = request.param['url']
    name = request.param['name']
    local_path = request.param['local_path']
    return url, name, local_path


@pytest.fixture(params=IMG_DATA_SETS)
def img_data_set(request):
    url = request.param['url']
    name = request.param['name']
    return url, name


@pytest.fixture(params=SRC_LIST_DATA_SET)
def src_list_data_set(request):
    url = request.param['url']
    src_list = request.param['src_list']
    local_path = request.param['local_path']
    return url, src_list, local_path


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as storage_dir:
        return storage_dir


@pytest.fixture
def get_file_content():
    def get_content(path):
        with open(path) as filename:
            return filename.read()
    return get_content


def test_get_page_source(get_file_content, url_data_set):
    url, name, local_path = url_data_set
    expected_result = get_file_content(local_path)
    result = _get_page_source(url)
    assert expected_result == result


def test_engine(temp_dir, get_file_content, url_data_set):
    url, name, local_path = url_data_set
    engine(temp_dir, url)
    result = get_file_content(os.path.join(temp_dir, name))
    expected_result = get_file_content(local_path)
    assert expected_result == result


def test_write_to_file(temp_dir, get_file_content, url_data_set):
    url, name, local_path = url_data_set
    text = get_file_content(local_path)
    _write_to_file(text, temp_dir, url)
    result = get_file_content(os.path.join(temp_dir, name))
    expected_result = get_file_content(local_path)
    assert expected_result == result


def test_get_storage_path(temp_dir, entity_data_set):
    url, entity_type, expected_name = entity_data_set
    result = get_storage_path(temp_dir, url, entity_type)
    expected_result = os.path.join(temp_dir, expected_name)
    assert expected_result == result


def test_parse_args(url_data_set):
    url, name, local_path = url_data_set
    result = parse_args(['-o=dodo', url])
    expected_result = ('dodo', url)
    assert expected_result == result


def test_download_img(temp_dir, img_data_set):
    url, name = img_data_set
    download_img(temp_dir, url)
    result_path = os.path.join(temp_dir, name)
    assert os.path.exists(result_path)


def test_get_src_list(get_file_content, src_list_data_set):
    url, src_list, local_path = src_list_data_set
    page_source = get_file_content(local_path)
    result = get_src_list(page_source)
    expected_result = src_list
    assert expected_result == result
