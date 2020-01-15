# flake8: noqa
import requests
import os
from page_loader.get_storage_path import get_storage_path
from bs4 import BeautifulSoup


def _get_page_source(url):
    response_object = requests.get(url)
    text = response_object.text
    return text


def _write_to_file(text, storage_dir, url):
    if not os.path.exists(storage_dir):
        os.makedirs(storage_dir)
    storage_path = get_storage_path(storage_dir, url, 'page')
    with open(storage_path, 'w') as storage_file:
        storage_file.write(text)


def get_src_list(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    src_list = []
    required_tag_names = ['link', 'script', 'img']
    all_tags = soup.findAll()
    for tag in all_tags:
        if tag.name in required_tag_names and tag.has_attr('src'):
            src_list.append(tag['src'])
    return src_list


def engine(storage_dir, url):
    page_source = _get_page_source(url)
    _write_to_file(page_source, storage_dir, url)


def download_img(storage_dir, url):
    if not os.path.exists(storage_dir):
        os.makedirs(storage_dir)
    storage_path = get_storage_path(storage_dir, url)
    with open(storage_path, 'wb') as storage:
        storage.write(requests.get(url).content)
