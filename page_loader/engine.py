import requests
import os
from page_loader.get_storage_path import get_storage_path


def _get_page_source(url):
    response_object = requests.get(url)
    text = response_object.text
    return text


def _write_to_file(text, storage_dir, url):
    if not os.path.exists(storage_dir):
        os.makedirs(storage_dir)
    storage_path = get_storage_path(storage_dir, url)
    with open(storage_path, 'w') as storage_file:
        storage_file.write(text)


def engine(storage_dir, url):
    page_source = _get_page_source(url)
    _write_to_file(page_source, storage_dir, url)
