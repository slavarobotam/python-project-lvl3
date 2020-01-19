import argparse
import os


DEFAULT_DIRECTORY = os.getcwd()  # perhaps 'pageloader_downloads' is better


def parse_args(argv):  # argument added for testability
    parser = argparse.ArgumentParser(description='Loading page utility')
    parser.add_argument('url')
    parser.add_argument('-o', '--output',
                        default=DEFAULT_DIRECTORY,
                        type=str,
                        help='Directory to store the page')
    args = parser.parse_args(argv)
    storage_dir = args.output
    url = args.url
    return storage_dir, url
