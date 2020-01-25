from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import requests
import logging
from page_loader.create_path import create_path

# sources to download: {tag_name: tag_attribute}
REQUIRED_TAGS = {
    'link': 'href',
    'script': 'src',
    'img': 'src'
}

logger = logging.getLogger()


def get_resources_data(page_source, url, dir_path):
    """Returns dictionary with resources data: type, url and local path."""
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

    logging.debug('Parsed url: {}'.format(urlparse(url)))
    for resource, data in resources_data.items():
        resource_url = urljoin(url, resource)
        logging.debug("Resource {}, url {}".format(resource, resource_url))
        if resource_url.startswith('//'):
            resource_url = '{}{}'.format('http:', resource_url)
        data['url'] = resource_url
        local_path = create_path(resource_url, dir_path)
        data['local_path'] = local_path
    return resources_data


def get_response(url, _type='text'):
    """Returns response object

    Raises exception for type 'text', if error occurred.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        if _type == 'text':
            logger.error('Error for url {}. Reason: {}'.format(url, str(err)))
            raise
        else:
            logger.warning('Skipping resource {}. '
                           'Reason: {}'.format(url, str(err)))
    else:
        logger.debug('Successfully received response from {}'.format(url))
        return response


def get_content(response, _type='text'):
    """Returns content based on source type: img or text"""
    url_content = response.content if _type == 'img' else response.text
    return url_content
