__version__ = "0.2.0"

from agarilog.log import get_logger


def reset_global_alog():
    global debug
    global info
    global warn
    global warning
    global error
    global critical
    default_logger = get_logger()
    debug = default_logger.debug
    info = default_logger.info
    warn = default_logger.warn
    warning = default_logger.warning
    error = default_logger.error
    critical = default_logger.critical


reset_global_alog()
