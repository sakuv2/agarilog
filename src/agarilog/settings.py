from typing import Optional

from pydantic import BaseSettings, validator


class LoggerSettings(BaseSettings):
    telegram_token: Optional[str]
    telegram_chat_id: Optional[int]
    telegram_level: str = "WARNING"
    slack_token: Optional[str]
    slack_channel: Optional[str]
    slack_level: str = "WARNING"
    chatwork_token: Optional[str]
    chatwork_room_id: Optional[int]
    chatwork_level: str = "WARNING"

    @validator("telegram_level", "slack_level", "chatwork_level")
    def _valid_level(cls, v):
        levels = ["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v not in levels:
            raise ValueError(
                f'{v} is not in ["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]'
            )
        return v

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
