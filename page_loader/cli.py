import argparse
import os

LEVELS = ['debug', 'info']


def parse_args(argv):  # argument added for testability
    default_dir = os.getcwd()
    parser = argparse.ArgumentParser(description='Loading page utility')
    parser.add_argument('url')
    parser.add_argument('-o', '--output',
                        default=default_dir,
                        type=str,
                        help='Directory to store the page')
    parser.add_argument('-l', '--level',
                        default='INFO',
                        choices=LEVELS,
                        help='Level of logging: ["debug", "info"]')
    args = parser.parse_args(argv)
    return args
