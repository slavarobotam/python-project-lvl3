import os
from page_loader.get_data import get_content


def download_resources(source_data):
    """Get urls and local_paths from source_data and download files"""
    for source, data in source_data.items():
        content = get_content(data['url'], data['type'])
        writing_mode = 'wb' if data['type'] == 'img' else 'w'
        write_to_file(content, data['local_path'], writing_mode)


def replace_paths(page_source, source_data):
    """Replace urls with local paths in main page source"""
    for source, data in source_data.items():
        page_source = page_source.replace(source, data['local_path'])
    return page_source


def write_to_file(content, storage_path, writing_mode='w'):
    """Save content considering writing mode, create dir if needed."""
    dir_path = os.path.dirname(storage_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(storage_path, writing_mode) as f:
        f.write(content)
