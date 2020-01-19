import argparse
import os


def parse_args(argv):  # argument added for testability
    default_dir = os.getcwd()  # perhaps 'my_downloads' is better choice
    parser = argparse.ArgumentParser(description='Loading page utility')
    parser.add_argument('url')
    parser.add_argument('-o', '--output',
                        default=default_dir,
                        type=str,
                        help='Directory to store the page')
    args = parser.parse_args(argv)
    storage_dir = args.output
    url = args.url
    return storage_dir, url
