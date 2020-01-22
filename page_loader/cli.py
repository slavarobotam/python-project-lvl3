import argparse
import os
import logging

level_config = {'debug': logging.DEBUG, 'info': logging.INFO}
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
                        help='Specify level of output verbosity')
    args = parser.parse_args(argv)
    stdout_level = level_config[args.level.lower()]

    logger = logging.getLogger()
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(filename)-20.20s] [%(levelname)-5.5s] %(message)s',
        filename='debug_log.log',
        filemode='w')

    format_for_stdout = logging.Formatter('%(message)s')
    format_for_logfile = logging.Formatter(
        '[%(filename)-18.18s] [%(levelname)-5.5s] %(message)s')

    handler_logfile = logging.FileHandler('debug_log.log', mode='w')
    handler_logfile.setLevel(logging.DEBUG)
    handler_logfile.setFormatter(format_for_logfile)

    handler_stdout = logging.StreamHandler()
    handler_stdout.setLevel(stdout_level)
    handler_stdout.setFormatter(format_for_stdout)

    logger.addHandler(handler_logfile)
    logger.addHandler(handler_stdout)

    logging.addLevelName(logging.INFO, logging.getLevelName(logging.INFO))
    logging.addLevelName(logging.ERROR, logging.getLevelName(logging.ERROR))
    return args
