from page_loader.create_path import create_path
from page_loader.get_data import get_resources_data, get_content
from page_loader.processing import (download_resources,
                                    replace_paths, write_to_file)
import logging

logger = logging.getLogger()


def engine(args):
    url, storage_dir = args.url, args.output

    page_source = get_content(url)
    page_localpath = create_path(url, storage_dir, entity_type='page')

    resources_data = get_resources_data(page_source, url, storage_dir)
    download_resources(resources_data, get_content, write_to_file)
    local_page_source = replace_paths(page_source, resources_data)

    write_to_file(local_page_source, page_localpath)
    logger.info('Page available locally at {}'.format(page_localpath))
