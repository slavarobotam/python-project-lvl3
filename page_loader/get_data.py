import requests
import logging


logger = logging.getLogger()


def check_scheme(url):
    """Adds scheme to url if it is missing."""
    if not url.startswith('http'):
        url = '{}{}'.format('http://', url)
    return url


def get_response(url, _type='text'):
    """Returns response object.

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
            logger.debug('Skipping resource {}. '
                         'Reason: {}'.format(url, str(err)))
    else:
        logger.debug('Successfully received response from {}'.format(url))
        return response


def get_content(response, _type='text'):
    """Returns content based on source type: img or text."""
    try:
        if _type == 'img':
            url_content = response.content
        else:
            response.encoding = 'utf-8'
            url_content = response.text
    except AttributeError:
        logger.debug("Can't get content from response object.")
    else:
        return url_content


def get_data(url):
    url_with_scheme = check_scheme(url)
    page_response = get_response(url_with_scheme)
    page_source = get_content(page_response)
    return page_source, url_with_scheme
