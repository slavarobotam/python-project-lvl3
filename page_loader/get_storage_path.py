import os

DELIMITER = '-'
EXTENSION = 'html'


def _get_storage_filename(url):
    normalised_url = os.path.normpath(url).lower()

    # remove scheme
    path_components = normalised_url.split(os.sep)
    del path_components[0]

    # replace punctuation with delimiter
    path_with_punctuation = DELIMITER.join(path_components)
    clean_name = ''
    for letter in path_with_punctuation:
        clean_name += (letter if letter.isalnum() else DELIMITER)

    # add extention to filename
    name_with_ext = '{}.{}'.format(clean_name, EXTENSION)

    return name_with_ext


def get_storage_path(dir, url):
    filename = _get_storage_filename(url)
    path = os.path.join(dir, filename)
    return path
