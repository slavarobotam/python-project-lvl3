import logging
import os

from page_loader.path import create_path

logger = logging.getLogger()


def ensure_dir(storage_dir):
    try:
        dir_path = os.path.join(os.getcwd(), str(storage_dir or ''))
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        logger.debug('Directory created: {}'.format(dir_path))
    except PermissionError:
        parent_dir = os.path.dirname(dir_path)
        logging.error('Permission denied for {}'.format(parent_dir))
        raise


def write_to_file(content, storage_path, writing_mode='w'):
    """Save content considering writing mode, create dir if needed."""
    try:
        with open(storage_path, writing_mode) as f:
            f.write(content)
            logger.debug('Content saved to {}'.format(storage_path))
    except FileNotFoundError as err:
        logging.error(
            'Error saving to {}. Error message: {}'.format(storage_path, err))
        raise FileNotFoundError(
            "FileNotFoundError occured, can't save file.") from err
    except PermissionError as err:
        logging.error(
            'Error saving to {}. Error message: {}'.format(storage_path, err))
        raise PermissionError(
            "PermissionError occured, can't save file.") from err
    except TypeError as err:
        logging.debug('TypeError while save attempt: {}'.format(err))


def save_data(url, storage_dir, local_page_source):
    page_localpath = create_path(url, storage_dir, entity_type='page')
    ensure_dir(storage_dir)
    write_to_file(local_page_source, page_localpath)
    logger.info('Page available locally at {}'.format(page_localpath))
