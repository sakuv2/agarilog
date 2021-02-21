import time

import agarilog as logger


def foo():
    bar()


def bar():
    return 1 / 0


logger.warning("warning", stack_info=True)

time.sleep(1)

try:
    foo()
except ZeroDivisionError:
    logger.critical("critical!!!", exc_info=True)
