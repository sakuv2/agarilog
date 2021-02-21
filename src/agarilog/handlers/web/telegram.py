import html
import logging
from datetime import datetime

from .._helper import get_other_info
from .web_handler import HTTPHandler


class TelegramHandler(HTTPHandler):
    def __init__(self, api_token: str, chat_id: int, **kwargs):
        self.chat_id = chat_id
        url = f"https://api.telegram.org/bot{api_token}/sendMessage"
        super().__init__(url, **kwargs)

    def mapLogRecord(self, record: logging.LogRecord) -> dict:
        level = TelegramStyled(record.levelname).b.u.s
        time = TelegramStyled(str(datetime.fromtimestamp(record.created))).i.b.u.s
        msg = record.getMessage()
        path = TelegramStyled(f"from: {record.pathname}:{record.lineno}").b.u.s
        other_info = get_other_info(record)
        text: str = level + " " + time + "\n" + path
        if msg != "":
            text += "\n" + msg
        if other_info is not None:
            text += "\n" + TelegramStyled(other_info).c.s

        return dict(chat_id=self.chat_id, parse_mode="HTML", text=text)


class TelegramStyled:
    def __init__(self, s: str):
        self.s = html.escape(s)

    @property
    def u(self) -> "TelegramStyled":
        self.s = f"<u>{self.s}</u>"
        return self

    @property
    def b(self) -> "TelegramStyled":
        self.s = f"<b>{self.s}</b>"
        return self

    @property
    def i(self) -> "TelegramStyled":
        self.s = f"<i>{self.s}</i>"
        return self

    @property
    def c(self) -> "TelegramStyled":
        self.s = f'<pre><code class="language-python">{self.s}</code></pre>'
        return self
