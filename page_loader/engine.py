from page_loader.create_path import create_path
from page_loader.get_data import get_resources_data, get_content
from page_loader.processing import (download_resources,
                                    replace_paths, write_to_file)
import logging

logger = logging.getLogger()


def engine(storage_dir, url):
    page_source = get_content(url)
    resources_dir_path = create_path(url, storage_dir, entity_type='dir')

    resources_data = get_resources_data(page_source, url, resources_dir_path)
    download_resources(resources_data, get_content, write_to_file)

    local_page_source = replace_paths(page_source, resources_data)
    page_path = create_path(url, storage_dir, entity_type='page')
    write_to_file(local_page_source, page_path)
    logger.info('Page available locally on {}'.format(page_path))
