import os

DELIMITER = '-'
EXTENSION = 'html'


def get_storage_path(storage_dir, url):
    normalised_url = os.path.normpath(url).lower()

    # remove scheme
    url_components = normalised_url.split(os.sep)
    del url_components[0]

    # replace non alphanumeric letters with delimiter
    non_alphanum_name = DELIMITER.join(url_components)
    name_with_delimiters = ''
    for letter in non_alphanum_name:
        name_with_delimiters += (letter if letter.isalnum() else DELIMITER)

    # add extention to filename
    name_with_ext = '{}.{}'.format(name_with_delimiters, EXTENSION)
    storage_path = os.path.join(storage_dir, name_with_ext)
    return storage_path
