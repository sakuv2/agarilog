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
