import logging
import os

LEVEL_CONFIG = {
    'debug': logging.DEBUG,
    'info': logging.INFO
    }


def run_logging(storage_dir, level):
    """
    Function enabling logging for both console output and log file.

    The level of console output verbosity is of user's choice.
    Logs for last call are always saved with debug level at debug_log.log
    in storage_dir specified by user.
    """
    stdout_level = LEVEL_CONFIG[level.lower()]

    logger = logging.getLogger()

    format_for_stdout = logging.Formatter('%(message)s')
    format_for_logfile = logging.Formatter(
        '[%(filename)-18.18s] [%(levelname)-5.5s] %(message)s')

    logfile_path = os.path.join(storage_dir, 'debug_log.log')
    handler_logfile = logging.FileHandler(logfile_path, mode='w')
    handler_logfile.setLevel(logging.DEBUG)
    handler_logfile.setFormatter(format_for_logfile)

    handler_stdout = logging.StreamHandler()
    handler_stdout.setLevel(stdout_level)
    handler_stdout.setFormatter(format_for_stdout)

    logger.addHandler(handler_logfile)
    logger.addHandler(handler_stdout)

    logging.getLogger().setLevel(logging.DEBUG)
