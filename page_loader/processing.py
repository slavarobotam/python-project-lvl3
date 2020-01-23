from page_loader.create_path import ensure_dir
import logging
import sys
from progress.bar import IncrementalBar

logger = logging.getLogger()


def download_resources(resources_data, dir_path,
                        get_content, save, need_dir=True):  # noqa: F811

    """
    Download files to dir_path according the paths in resources dictionary.

    Creates directory if need_dir is True.
    Functions 'get_content' and 'save' added for testability.
    """
    if need_dir and resources_data:
        ensure_dir(dir_path)
    try:
        total_items = len(resources_data)
        bar_width = 30
        bar = IncrementalBar('Downloading:', max=bar_width)
        bar.suffix = '%(percent).1f%% (eta: %(eta)s)'

        filled_bar = 0
        processed_percentage = 0
        for source, data in resources_data.items():
            content = get_content(data['url'], data['type'])
            writing_mode = 'wb' if data['type'] == 'img' else 'w'
            save(content, data['local_path'], writing_mode)
            processed_percentage += (1 / total_items)
            if processed_percentage >= filled_bar / bar_width:
                bar.next()
                filled_bar += 1
        bar.finish()
        logger.info('All resources downloaded successfully.')
    except AttributeError:
        logger.debug('Downloading skipped.')


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
    except OSError as err:
        logging.error(
            'Error saving to {}. Error message: {}'.format(storage_path, err))
        sys.exit(1)
