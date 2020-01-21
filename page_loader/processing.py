# flake8: noqa: F811
import os
from page_loader.get_data import get_content
import logging

logger = logging.getLogger()


def download_resources(resources_data, get_content, write_to_file):
    """
    Download files according the paths in resources dictionary.

    Functions 'write_to_file' and 'get_content' added for testability.
    """
    try:
        for source, data in resources_data.items():
            content = get_content(data['url'], data['type'])
            writing_mode = 'wb' if data['type'] == 'img' else 'w'
            write_to_file(content, data['local_path'], writing_mode)
        logger.info('All resources downloaded successfully.')
    except AttributeError:
       logger.warning('Downloading skipped.')


def replace_paths(page_source, resources_data):
    """Replace urls with local paths in main page source"""
    try:
        for source, data in resources_data.items():
            page_source = page_source.replace(source, data['local_path'])
        logger.debug('Urls replaced with local paths.')
    except AttributeError:
        logger.warning('Path replacing skipped.')
    return page_source


def write_to_file(content, storage_path, writing_mode='w'):
    """Save content considering writing mode, create dir if needed."""
    dir_path = os.path.dirname(storage_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        logger.info('Directory created: {}'.format(dir_path))
    try:
        with open(storage_path, writing_mode) as f:
            f.write(content)
            logger.debug('Content saved to {}'.format(storage_path))
    except IOError as e:
        logging.warning("Error saving to {}. Error: {}".format(storage_path, e))
