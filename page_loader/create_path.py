import logging
import os
from urllib.parse import urlparse

DELIMITER = '-'
SPECIAL_ENTITY_TYPES = {
    'dir': '_files',
    'page': '.html'
}

logger = logging.getLogger()


def make_alphanum(name):
    """Replace all non-alphanumeric characters with delimeter"""
    alphanum_name = ''
    for letter in name:
        alphanum_name += (letter if letter.isalnum() else DELIMITER)
    return alphanum_name


def create_path(url, storage_dir, entity_type=None):
    """Create name from url for the required entity type: page, dir or None.

    If entity type is not None, add appropriate ending.
    Otherwise filename retains the original extension if there is one.
    """
    normalised_url = os.path.normpath(url)

    # remove scheme
    parsed = urlparse(normalised_url)
    scheme = '{}:/'.format(parsed.scheme)
    full_path = normalised_url.replace(scheme, '', 1)

    # if relative path used, remove leading punctuation
    full_path = full_path.replace('..', '').strip('/')

    # path processing according to entity type
    root, ext = os.path.splitext(full_path)
    if entity_type is not None:
        alphanum_name = make_alphanum(full_path)
        ending = SPECIAL_ENTITY_TYPES[entity_type]
    else:
        alphanum_name = make_alphanum(root)
        ending = ext

    full_name = '{}{}'.format(alphanum_name, ending)
    path = os.path.join(os.getcwd(), storage_dir, full_name)
    logger.debug('Path created: {}'.format(path))
    return path
