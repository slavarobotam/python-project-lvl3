import requests
import os
from page_loader.get_storage_path import get_path
from page_loader.download_resources import (
    get_source_data, get_resources_paths, download_resources, replace_paths)


def get_page_source(url):
    response_object = requests.get(url)
    text = response_object.text
    return text


def write_to_file(content, storage_path, writing_mode='w'):
    dir_path = os.path.dirname(storage_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(storage_path, writing_mode) as f:
        f.write(content)


def engine(storage_dir, url):
    # get page content
    page_source = get_page_source(url)

    # download resources
    source_dir_path = get_path(url, storage_dir, entity='dir')
    source_data = get_source_data(page_source)
    resources_paths = get_resources_paths(source_data, url, source_dir_path)
    download_resources(resources_paths)
    page_source = replace_paths(page_source, resources_paths)

    # save page
    page_path = get_path(url, storage_dir, entity='page')
    write_to_file(page_source, page_path)
