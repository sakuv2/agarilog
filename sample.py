import time

import agarilog as logger


def foo():
    bar()


def bar():
    return 1 / 0


logger.warning("warning", stack_info=True)

time.sleep(0.1)

try:
    foo()
except ZeroDivisionError:
    logger.error("error!!!", exc_info=True)


logger.debug("debug")
logger.info("info")
logger.warning("warning")
logger.error("error")
logger.critical("critical")
