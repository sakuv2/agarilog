from enum import Enum
from typing import Optional

from pydantic import BaseSettings


class Level(str, Enum):
    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class StremaType(str, Enum):
    NONE = "NONE"
    PRINT = "PRINT"
    NORMAL = "NORMAL"
    COLOR = "COLOR"


class LoggerSettings(BaseSettings):
    telegram_token: Optional[str]
    telegram_chat_id: Optional[int]
    telegram_level: Level = Level.WARNING
    slack_token: Optional[str]
    slack_channel: Optional[str]
    slack_level: Level = Level.WARNING
    chatwork_token: Optional[str]
    chatwork_room_id: Optional[int]
    chatwork_level: Level = Level.WARNING

    stream_type: str = StremaType.NONE
    stream_level: Level = Level.WARNING

    @property
    def use_telegram(self) -> bool:
        return self._check_none("telegram")

    @property
    def use_slack(self) -> bool:
        return self._check_none("slack")

    @property
    def use_chatwork(self) -> bool:
        return self._check_none("chatwork")

    def _check_none(self, pre_fix: str) -> bool:
        arr = [v for k, v in dict(self).items() if pre_fix in k]
        return all(arr)

    class Config:
        env_prefix = "log_"
        env_file = ".env"
        env_file_encoding = "utf-8"
