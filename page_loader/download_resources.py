from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from page_loader.get_storage_path import get_path
from page_loader.engine import write_to_file


def get_source_data(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    source_data = {}
    required_tags = {'link': 'href', 'script': 'src', 'img': 'src'}
    all_tags = soup.findAll()
    for tag in all_tags:
        if tag.name in required_tags:
            required_attr = required_tags[tag.name]
            if tag.has_attr(required_attr):
                source = tag[required_attr]
                source_data[source] = {'type': tag.name}
    return source_data


def get_resources_paths(source_data, url, source_dir_path):
    for source, data in source_data.items():
        source_url = urljoin(url, source)
        data['url'] = source_url

        local_path = get_path(source_url, source_dir_path)
        data['local_path'] = local_path
    return source_data


def download_resources(source_data):
    for source, data in source_data.items():
        r = requests.get(data['url'], allow_redirects=True)
        content = r.content if data['type'] == 'img' else r.text
        writing_mode = 'wb' if data['type'] == 'img' else 'w'
        write_to_file(content, data['local_path'], writing_mode)


def replace_paths(page_source, resources_paths):
    # replace urls with local paths
    for source, data in resources_paths.items():
        page_source = page_source.replace(source, data['local_path'])
    return page_source
