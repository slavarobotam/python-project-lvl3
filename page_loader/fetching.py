import logging

import requests

logger = logging.getLogger()


def ensure_scheme(url):
    """Adds scheme to url if it is missing."""
    if not url.startswith('http'):
        url = '{}{}'.format('http://', url)
    return url


def get_response(url, _type='text'):
    """Returns response object.

    Raises exception for type 'text', if error occurred.
    Skipping for other types.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.RequestException) as err:
        if _type == 'text':
            logger.error('Error for url {}. Please choose another one. '
                         'Reason: {}'.format(url, err))
            raise
        else:
            logger.debug('Skipping resource {}. '
                         'Reason: {}'.format(url, err))
    else:
        logger.debug('Successfully received response from {}'.format(url))
        return response


def get_content(response, _type='text'):
    """Returns content based on source type: img or text."""
    try:
        if _type == 'img':
            url_content = response.content
        else:
            response.encoding = response.apparent_encoding
            url_content = response.text
    except AttributeError as err:
        logger.debug("Error getting content: {}".format(err))
    else:
        return url_content


def fetch_data(url, get_response, get_content):
    url_with_scheme = ensure_scheme(url)
    page_response = get_response(url_with_scheme)
    page_source = get_content(page_response)
    logger.debug('Successfully received data from {}'.format(url))
    return page_source, url_with_scheme
