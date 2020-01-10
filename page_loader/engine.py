import argparse
import requests
import os
from page_loader.get_storage_path import get_storage_path

DEFAULT_DIRECTORY = os.getcwd()

parser = argparse.ArgumentParser(description='Loading page utility')
parser.add_argument('url')
parser.add_argument('-o', '--output',
                    default=DEFAULT_DIRECTORY,
                    type=str,
                    help='Directory to store the page')


def write_to_file(url, storage_path):
    response_object = requests.get(url)
    text = response_object.text
    with open(storage_path, 'w') as storage_file:
        storage_file.write(text)


def engine(args):
    url = args.url
    dir = args.output
    storage_path = get_storage_path(dir, url)
    write_to_file(url, storage_path)
