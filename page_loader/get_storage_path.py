import os
from urllib.parse import urlparse


DELIMITER = '-'
PAGE = 'page'
DIR = 'dir'
SPECIAL_ENTITY_TYPES = {
    DIR: '_files',
    PAGE: '.html'
}


def _get_alphanum_name(path):
    """Replace all non-alphanumeric characters with delimeter"""
    alphanum_name = ''
    for letter in path:
        alphanum_name += (letter if letter.isalnum() else DELIMITER)
    return alphanum_name


def get_storage_path(storage_dir, url, entity_type=None):
    """Generates storage path for the required entity type.

    If entity type is in SPECIAL_ENTITY_TYPES, adds appropriate ending
    to the path.
    Otherwise path retains the original extension if there is one.
    """
    normalised_url = os.path.normpath(url)
    parsed_url = urlparse(normalised_url)

    # remove scheme
    scheme = '{}:/'.format(parsed_url.scheme)
    full_path = normalised_url.replace(scheme, '', 1)

    # process path according to enity type
    root, ext = os.path.splitext(full_path)
    if entity_type:
        alphanum_name = _get_alphanum_name(full_path)
        ending = SPECIAL_ENTITY_TYPES[entity_type]
    else:
        alphanum_name = _get_alphanum_name(root)
        ending = ext

    full_name = '{}{}'.format(alphanum_name, ending)
    storage_path = os.path.join(storage_dir, full_name)
    return storage_path
