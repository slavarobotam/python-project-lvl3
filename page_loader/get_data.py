from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import logging
import sys
from page_loader.create_path import create_path

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

    if not resources_data:
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
    except (
            requests.ConnectionError,
            requests.RequestException,
            requests.HTTPError,
            requests.Timeout,
            requests.TooManyRedirects) as err:
        logger.error(
            'Error for url {}. Message: {}.\
            Please choose another one.'.format(url, str(err)),
            exc_info=False)  # set True to see traceback
        sys.exit(1)
    else:
        url_content = r.content if _type == 'img' else r.text
        logger.debug('Successfully got content from {}'.format(url))
        return url_content
