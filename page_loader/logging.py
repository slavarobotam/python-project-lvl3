import logging
import os
from page_loader.create_path import ensure_dir

LEVEL_CONFIG = {
    'debug': logging.DEBUG,
    'info': logging.INFO
}


def run_logging(args):
    """
    Function enabling logging for both console output and log file.

    The level of console output verbosity is of user's choice.
    Logs for last call are always saved with debug level at debug_log.log
    in storage_dir specified by user.
    """
    logger = logging.getLogger()

    if args.filepath:
        logfile_path = os.path.join(os.getcwd(), args.filepath)

        if logfile_path.endswith(('log', 'txt')):
            ensure_dir(os.path.dirname(logfile_path))
        else:
            ensure_dir(logfile_path)
            logfile_path = os.path.join(logfile_path, 'debug.log')

        handler_logfile = logging.FileHandler(logfile_path, mode='w')
        handler_logfile.setLevel(logging.DEBUG)
        format_for_logfile = logging.Formatter(
            '[%(filename)-18.18s] [%(levelname)-5.5s] %(message)s')
        handler_logfile.setFormatter(format_for_logfile)
        logger.addHandler(handler_logfile)

    handler_stdout = logging.StreamHandler()
    stdout_level = LEVEL_CONFIG[args.level.lower()]
    handler_stdout.setLevel(stdout_level)
    format_for_stdout = logging.Formatter('%(message)s')
    handler_stdout.setFormatter(format_for_stdout)
    logger.addHandler(handler_stdout)

    logging.getLogger().setLevel(logging.DEBUG)
