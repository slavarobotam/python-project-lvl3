from page_loader.create_path import create_path, ensure_dir
from page_loader.get_data import get_resources_data, get_content, get_response
from page_loader.processing import (download_resources, check_scheme,
                                    replace_paths, save)
from page_loader.logging import run_logging
import logging

logger = logging.getLogger()


def engine(args):
    run_logging(args)

    ensure_dir(args.output)

    url = check_scheme(args.url)
    page_response = get_response(url)
    page_source = get_content(page_response)
    page_localpath = create_path(url, args.output, entity_type='page')

    resources_dir_path = create_path(url, args.output, entity_type='dir')
    resources_data = get_resources_data(page_source, url, resources_dir_path)
    download_resources(resources_data, resources_dir_path,
                       get_response, get_content, save)
    local_page_source = replace_paths(page_source, resources_data)

    save(local_page_source, page_localpath)
    logger.info('Page available locally at {}'.format(page_localpath))
