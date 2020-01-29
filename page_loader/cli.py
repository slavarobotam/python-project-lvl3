import argparse
import os

from page_loader.logging import run_logging

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
                        help='Level of output logging: ["debug", "info"]')
    parser.add_argument('-f', '--filepath',
                        action='store',
                        nargs='?',
                        const='debug.log',
                        type=str,
                        help='Path to log file, for example temp/mylog.log')

    args = parser.parse_args(argv)
    return args


def run_cli(argv):
    args = parse_args(argv)
    run_logging(args.level, args.filepath)
    return args
