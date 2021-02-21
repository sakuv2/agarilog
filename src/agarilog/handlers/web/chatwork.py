import logging
from datetime import datetime

from .._helper import get_other_info
from .web_handler import HTTPHandler

cw_msg = """[info][title]{level_name} {time}
{path_name}:{line_no}
[/title]
{msg}{other_info}
[/info]
"""


def code(s: str) -> str:
    return f"[code]{s}[/code]"


class ChatworkHandler(HTTPHandler):
    def __init__(self, token: str, room_id: int, **kwargs):
        url = f"https://api.chatwork.com/v2/rooms/{room_id}/messages"
        headers = {"X-ChatWorkToken": token}
        super().__init__(url, headers, mode="data", **kwargs)

    def mapLogRecord(self, record: logging.LogRecord) -> dict:
        self.format(record)
        other_info = get_other_info(record)
        other_info = "" if other_info is None else "[hr]" + code(other_info)

        msg = cw_msg.format(
            level_name=record.levelname,
            time=str(datetime.fromtimestamp(record.created)),
            path_name=record.pathname,
            line_no=record.lineno,
            msg="" if record.msg == "" else code(record.msg),
            other_info=other_info,
        )

        return {"body": msg}
