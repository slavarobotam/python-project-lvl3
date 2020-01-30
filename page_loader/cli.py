import argparse

from page_loader.logging import DEFAULT_STDOUT_LEVEL, LEVELS


def parse_args(argv):
    parser = argparse.ArgumentParser(description='Loading page utility')
    parser.add_argument('url')
    parser.add_argument('-o', '--output',
                        default=None,
                        type=str,
                        help='Directory to store the page')
    parser.add_argument('-l', '--level',
                        default=DEFAULT_STDOUT_LEVEL,
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
