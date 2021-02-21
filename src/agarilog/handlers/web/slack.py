import logging

from .._helper import get_other_info
from .web_handler import HTTPHandler


class SlcakHandler(HTTPHandler):
    def __init__(self, token: str, channel: str, **kwargs):
        self.channel = channel
        url = "https://slack.com/api/chat.postMessage"
        headers = {"Authorization": f"Bearer {token}"}
        super().__init__(url, headers, **kwargs)

    def mapLogRecord(self, record: logging.LogRecord) -> dict:
        loglevel_color = {
            "DEBUG": "gray",
            "INFO": "good",
            "WARNING": "warning",
            "ERROR": "#E91E63",
            "CRITICAL": "danger",
        }
        self.format(record)
        text = record.msg
        other_info = get_other_info(record)
        if other_info is not None:
            text += "\n" + f"```{other_info}```"

        content = dict(
            ts=record.created,
            text=text,
            color=loglevel_color.get(record.levelname, "white"),
            footer=f"{record.pathname}:{record.lineno} [{record.levelname}]",
        )

        return dict(attachments=[content], channel=self.channel)
