import logging
import os

from page_loader.storing import ensure_dir

LEVELS = (DEBUG, INFO) = ('debug', 'info')
LEVEL_CONFIG = {
    DEBUG: logging.DEBUG,
    INFO: logging.INFO
}
DEFAULT_LOGFILE_LEVEL = DEBUG
DEFAULT_STDOUT_LEVEL = INFO


def run_logging(level, filepath):
    """
    Function enabling logging for both console output and log file.

    The level of console output verbosity is of user's choice.

    If filepath specified, creates logfile there. If only directory specified,
    there will be created file 'debug.log'. Log level always 'debug'.
    If only flag `-f` specified, in cwd will be created file `debug.log`.
    """
    logger = logging.getLogger()

    if filepath:
        logfile_path = os.path.join(os.getcwd(), filepath)

        if logfile_path.endswith(('log', 'txt')):
            ensure_dir(os.path.dirname(logfile_path))
        else:
            ensure_dir(logfile_path)
            logfile_path = os.path.join(logfile_path, 'debug.log')

        handler_logfile = logging.FileHandler(logfile_path, mode='w')
        logfile_level = LEVEL_CONFIG[DEFAULT_LOGFILE_LEVEL]
        handler_logfile.setLevel(logfile_level)
        format_for_logfile = logging.Formatter(
            '%(asctime)s | %(filename)-18.18s | %(levelname)-5.5s | '
            '%(message)s')
        handler_logfile.setFormatter(format_for_logfile)
        logger.addHandler(handler_logfile)

    handler_stdout = logging.StreamHandler()
    stdout_level = LEVEL_CONFIG[level.lower()]
    handler_stdout.setLevel(stdout_level)
    format_for_stdout = logging.Formatter('%(message)s')
    handler_stdout.setFormatter(format_for_stdout)
    logger.addHandler(handler_stdout)

    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug('Logging works fine')
