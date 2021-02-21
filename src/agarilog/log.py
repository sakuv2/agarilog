import logging

from .handlers import ChatworkHandler, SlcakHandler, TelegramHandler
from .settings import LoggerSettings


def get_logger(env_file: str = ".env"):
    conf = LoggerSettings(_env_file=env_file)
    logger = logging.getLogger("")
    logger.setLevel(0)
    if conf.use_telegram:
        th = TelegramHandler(api_token=conf.telegram_token, chat_id=conf.telegram_chat_id)
        th.setLevel(conf.telegram_level)
        logger.addHandler(th)

    if conf.use_slack:
        sh = SlcakHandler(token=conf.slack_token, channel=conf.slack_channel)
        sh.setLevel(conf.slack_level)
        logger.addHandler(sh)

    if conf.use_chatwork:
        ch = ChatworkHandler(token=conf.chatwork_token, room_id=conf.chatwork_room_id)
        sh.setLevel(conf.chatwork_level)
        logger.addHandler(ch)

    return logger
