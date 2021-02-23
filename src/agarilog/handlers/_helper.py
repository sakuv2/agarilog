import io
import logging
import traceback
from typing import Optional


def get_other_info(record: logging.LogRecord) -> Optional[str]:
    """stack_infoかexec_info(traceback)を取り出す

    Args:
        record (logging.LogRecord): レコード

    Returns:
        Optional[str]: traceback or exec_info or None
    """
    if record.exc_text is not None:
        return record.exc_text
    elif record.exc_info is not None:
        ei = record.exc_info
        with io.StringIO() as sio:
            traceback.print_exception(ei[0], ei[1], ei[2], None, sio)
            return sio.getvalue()
    elif record.stack_info is not None:
        return record.stack_info
    return None


_color_map = {
    0: "0m",
    10: "0;36m",
    20: "0;32m",
    30: "0;33m",
    40: "0;31m",
    50: "1;31m",
}


def color(level: int, msg: str) -> str:
    level = level // 10 * 10
    return f"\x1b[{_color_map[level]}{msg}\x1b[0m"


def light_blue(msg: str) -> str:
    return f"\x1b[0;36m{msg}\x1b[0m"
