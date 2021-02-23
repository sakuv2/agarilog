import logging
import sys

from .handlers import ChatworkHandler, SlcakHandler, TelegramHandler
from .handlers.formatter import ColofulFormatter
from .settings import LoggerSettings, StremaType


def get_logger(name: str = "agarilog", env_file: str = ".env"):
    conf = LoggerSettings(_env_file=env_file)
    logger = logging.getLogger(name)
    logger.setLevel(0)
    if conf.use_telegram:
        th = TelegramHandler(api_token=conf.telegram_token, chat_id=conf.telegram_chat_id)
        th.setLevel(conf.telegram_level.value)
        logger.addHandler(th)

    if conf.use_slack:
        sh = SlcakHandler(token=conf.slack_token, channel=conf.slack_channel)
        sh.setLevel(conf.slack_level.value)
        logger.addHandler(sh)

    if conf.use_chatwork:
        ch = ChatworkHandler(token=conf.chatwork_token, room_id=conf.chatwork_room_id)
        sh.setLevel(conf.chatwork_level.value)
        logger.addHandler(ch)

    set_stream_handler(logger, conf)

    return logger


def set_stream_handler(logger: logging.Logger, conf: LoggerSettings):
    st = logging.StreamHandler(sys.stdout)
    st.setLevel(conf.stream_level.value)

    if conf.stream_type == StremaType.NONE:
        return
    if conf.stream_type == StremaType.PRINT:
        formatter = get_print_formatter()
    if conf.stream_type == StremaType.NORMAL:
        formatter = get_normal_formatter()
    if conf.stream_type == StremaType.COLOR:
        formatter = get_colorfull_formatter()
    st.setFormatter(formatter)

    logger.addHandler(st)


def get_print_formatter():
    fmt = "%(message)s"
    formatter = logging.Formatter(fmt=fmt)
    return formatter


def get_normal_formatter():
    fmt = "%(levelname)s %(asctime)s %(pathname)s:%(lineno)s %(message)s"
    formatter = logging.Formatter(fmt=fmt)
    return formatter


def get_colorfull_formatter():
    fmt = "%(levelname)s %(asctime)s %(pathname)s:%(lineno)s %(message)s"
    formatter = ColofulFormatter(fmt=fmt)
    return formatter
