from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from page_loader.create_path import create_path
import logging


# sources to download: {tag_name: tag_attribute}
REQUIRED_TAGS = {
    'link': 'href',
    'script': 'src',
    'img': 'src'
}

logger = logging.getLogger()


def get_resources_data(page_source, url, dir_path):
    """Returns dictionary with info about resources."""
    soup = BeautifulSoup(page_source, 'html.parser')
    resources_data = {}
    for tag in soup.findAll():
        if tag.name in REQUIRED_TAGS:
            required_attr = REQUIRED_TAGS[tag.name]
            if tag.has_attr(required_attr):
                resource = tag[required_attr]
                resources_data[resource] = {'type': tag.name}

    if resources_data == {}:
        logging.warning("No resources to download.")
        return None

    for resource, data in resources_data.items():
        resource_url = urljoin(url, resource)
        data['url'] = resource_url
        local_path = create_path(resource_url, dir_path)
        data['local_path'] = local_path
    return resources_data


def get_content(url, _type='text'):
    """Returns content based on source type: img or text"""
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.critical('Error in the request: {}'.format(e))
        raise
    else:
        url_content = r.content if _type == 'img' else r.text
        logger.debug('Successfully got content from {}'.format(url))
        return url_content
