from page_loader.create_path import ensure_dir
import logging
from progress.bar import IncrementalBar

logger = logging.getLogger()
BAR_WIDTH = 30


def download_resources(resources, dir_path, get_response,
                        get_content, save, need_dir=True):  # noqa: F811
    """
    Download files to dir_path according the paths in resources dictionary.

    Creates directory if need_dir is True.
    Functions 'get_response', 'get_content' and 'save' added for testability.
    """
    if resources is None:
        logger.debug('Downloading skipped.')
        return None

    if need_dir:
        ensure_dir(dir_path)

    bar = IncrementalBar('Downloading:', max=BAR_WIDTH)
    bar.suffix = '%(percent).1f%% (Time to completion: %(eta)s seconds)'
    for i in bar.iter(resources.items()):
        for source, data in resources.items():
            response = get_response(data['url'], data['type'])
            content = get_content(response, data['type'])
            writing_mode = 'wb' if data['type'] == 'img' else 'w'
            save(content, data['local_path'], writing_mode)
    logger.info('Resources downloaded successfully.')


def replace_paths(page_source, resources_data):
    """Replace urls with local paths in main page source"""
    try:
        for source, data in resources_data.items():
            page_source = page_source.replace(source, data['local_path'])
        logger.debug('Urls replaced with local paths.')
    except AttributeError:
        logger.debug('Path replacing skipped.')
    return page_source


def save(content, storage_path, writing_mode='w'):
    """Save content considering writing mode, create dir if needed."""
    try:
        with open(storage_path, writing_mode) as f:
            f.write(content)
            logger.debug('Content saved to {}'.format(storage_path))
    except FileNotFoundError as err:
        logging.error(
            'Error saving to {}. Error message: {}'.format(storage_path, err))
        raise FileNotFoundError("FileNotFoundError occured, can't save file.")
    except PermissionError as err:
        logging.error(
            'Error saving to {}. Error message: {}'.format(storage_path, err))
        raise PermissionError("PermissionError occured, can't save file.")
    except TypeError as err:
        logging.debug('TypeError while save attempt: {}'.format(err))


def check_scheme(url):
    if not url.startswith('http'):
        url = '{}{}'.format('http://', url)
    return url
