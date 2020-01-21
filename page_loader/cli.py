import argparse
import os
import logging

LEVELS = ('debug', 'info', 'warning', 'error', 'critical')


def parse_args(argv):  # argument added for testability
    default_dir = os.getcwd()
    parser = argparse.ArgumentParser(description='Loading page utility')
    parser.add_argument('url')
    parser.add_argument('-o', '--output',
                        default=default_dir,
                        type=str,
                        help='Directory to store the page')
    parser.add_argument('-l', '--log-level',
                        default='INFO',
                        choices=LEVELS)
    args = parser.parse_args(argv)
    logging.basicConfig(
        level=args.log_level.upper(),
        format="[%(filename)-20.20s] [%(levelname)-5.5s] %(message)s",
        handlers=[
            logging.FileHandler('mylog.log', mode='w'),  # 'w' or 'a'
            logging.StreamHandler()
        ])
    return args
