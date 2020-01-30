import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from progress.bar import IncrementalBar

from page_loader.fetching import ensure_scheme, get_content, get_response
from page_loader.path import normalize
from page_loader.storing import ensure_dir, write_to_file

logger = logging.getLogger()

# sources to download: {tag_name: tag_attribute}
REQUIRED_TAGS = {
    'link': 'href',
    'script': 'src',
    'img': 'src'
}
BAR_WIDTH = 30


def get_resources_data(page_source, url):
    """Returns dictionary with resources data: type, url and local path."""
    soup = BeautifulSoup(page_source, 'html.parser')
    resources_data = {}
    for tag in soup.findAll():
        if tag.name in REQUIRED_TAGS:
            required_attr = REQUIRED_TAGS[tag.name]
            if tag.has_attr(required_attr):
                resource = tag[required_attr]
                resources_data[resource] = {'type': tag.name}
    return resources_data


def make_paths(resources_data, url, dir_path):
    """Creates urls and local paths for resources, adds to dict."""
    for resource, data in resources_data.items():
        resource_url = urljoin(url, resource)
        logging.debug("Resource {}, url {}".format(resource, resource_url))
        ensure_scheme(resource_url)
        data['url'] = resource_url
        local_path = normalize(resource_url, dir_path)
        data['local_path'] = local_path
    return resources_data


def download(resources_data, dir_path, get_response,
                        get_content, save, need_dir=True):  # noqa: F811
    """
    Download files to dir_path according the paths in resources dictionary.

    Creates directory if need_dir is True.
    Functions 'get_response', 'get_content' and 'save' added for testability.
    """
    if resources_data is None:
        logger.debug('Downloading skipped.')
        return None

    if need_dir:
        ensure_dir(dir_path)

    bar = IncrementalBar('Downloading:', max=BAR_WIDTH)
    bar.suffix = '%(percent).1f%% (Time to completion: %(eta)s seconds)'
    for i in bar.iter(resources_data.items()):
        for source, data in resources_data.items():
            response = get_response(data['url'], data['type'])
            content = get_content(response, data['type'])
            writing_mode = 'wb' if data['type'] == 'img' else 'w'
            save(content, data['local_path'], writing_mode)
    logger.info('Resources downloaded successfully.')


def replace_paths(page_source, resources_data):
    """Replace urls with local paths in main page source."""
    try:
        for source, data in resources_data.items():
            page_source = page_source.replace(source, data['local_path'])
        logger.debug('Urls replaced with local paths.')
    except AttributeError:
        logger.debug('Path replacing skipped.')
    return page_source


def process_data(page_source, url, storage_dir, download, normalize):
    resources_data = get_resources_data(page_source, url)
    if resources_data:
        resources_dir_path = normalize(url, storage_dir, entity_type='dir')
        resources_data = make_paths(resources_data, url, resources_dir_path)
        download(resources_data, resources_dir_path, get_response, get_content,
                 write_to_file)
        local_page_source = replace_paths(page_source, resources_data)
    else:
        logging.warning("No resources to download.")
        local_page_source = page_source
    return local_page_source
