import logging

from .request_backend import RequestBackend

rb = RequestBackend()


class HTTPHandler(logging.Handler):
    def __init__(self, url: str, headers: dict = {}, mode: str = "json", **kwargs):
        """これを継承して、各WebサービスにあったHanderを作成する

        Args:
            url (str): ログを送るサービスのエンドポイント
            headers (Optional[dict], optional): ヘッダー(認証用). Defaults to None.
            mode (Literal["json", "data"], optional): mode. Defaults to "json".
        """
        self.url = url
        self.headers = headers
        self.mode = mode
        self.rb = rb
        self.rb.init()

        super().__init__(**kwargs)

    def mapLogRecord(self, record: logging.LogRecord) -> dict:
        return {k: v for k, v in record.__dict__.items() if isinstance(v, str)}

    def emit(self, record: logging.LogRecord) -> None:
        kwargs = {
            "url": self.url,
            self.mode: self.mapLogRecord(record),
            "headers": self.headers,
        }
        self.rb.post(**kwargs)
