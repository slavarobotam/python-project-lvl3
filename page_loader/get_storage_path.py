import os
from urllib.parse import urlparse


DELIMITER = '-'
SPECIAL_ENTITY_TYPES = {
    'dir': '_files',
    'page': '.html'
}


def make_alphanum(name):
    """Replace all non-alphanumeric characters with delimeter"""
    alphanum_name = ''
    for letter in name:
        alphanum_name += (letter if letter.isalnum() else DELIMITER)
    return alphanum_name


def get_path(url, storage_dir, entity=None):
    """Creates name from path for the required entity type.

    If entity type is in SPECIAL_ENTITY_TYPES, adds appropriate ending.
    Otherwise filename retains the original extension if there is one.
    """
    normalised_url = os.path.normpath(url)

    # remove scheme
    parsed = urlparse(normalised_url)
    scheme = '{}:/'.format(parsed.scheme)
    full_path = normalised_url.replace(scheme, '', 1)

    # if relative path, remove leading punctuation
    full_path = full_path.replace('..', '').strip('/')

    # process path according to entity type
    root, ext = os.path.splitext(full_path)
    if entity:
        alphanum_name = make_alphanum(full_path)
        ending = SPECIAL_ENTITY_TYPES[entity]
    else:
        alphanum_name = make_alphanum(root)
        ending = ext

    # add proper ending
    full_name = '{}{}'.format(alphanum_name, ending)

    path = os.path.join(os.getcwd(), storage_dir, full_name)
    return path
