import logging
from copy import copy
from datetime import datetime
from typing import Optional

from ._helper import color, light_blue


class Formatter(logging.Formatter):
    def formatTime(self, record: logging.LogRecord, datefmt: Optional[str] = None) -> str:
        ct = datetime.fromtimestamp(record.created)
        if datefmt is None:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = f"{t}.{int(record.msecs):03}"
        else:
            s = ct.strftime(datefmt)
        return s


level_map = {
    0: "T",
    10: "D",
    20: "I",
    30: "W",
    40: "E",
    50: "C",
}


class ColofulFormatter(Formatter):
    def format(self, record: logging.LogRecord):
        level = record.levelno // 10 * 10
        r = copy(record)
        r.levelname = color(level, level_map[r.levelno])
        r.pathname = light_blue(r.pathname)
        r.lineno = light_blue(str(r.lineno))
        return super().format(r)

    def formatTime(self, record: logging.LogRecord, datefmt: Optional[str] = None) -> str:
        return color(record.levelno, super().formatTime(record, datefmt=datefmt))
