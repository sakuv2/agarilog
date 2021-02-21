agarilog
========

|PyPI version| |Python Versions|

.. |PyPI version| image:: https://badge.fury.io/py/polar-bear.svg
    :target: https://pypi.org/project/agarilog/
    :alt: PyPI version

.. |Python versions| image:: https://img.shields.io/pypi/pyversions/agarilog.svg
    :target: https://pypi.org/project/agarilog/
    :alt: Python versions


This is simple logger for message service.

Installation
------------

.. code-block::

    pip install agarilog

Features
--------

Use .env file.
##############################

.. code-block:: python

    >>> import agarilog as logger
    >>> logger.info("Hello agarilog!")

Use any .env file.
##########################

.. code-block:: python

    >>> from agarilog import get_logger
    >>> logger = get_logger("dev.env")
    >>> logger.info("Hello agarilog!")

This is use :code:`dev.env` file.

Telegram
########

.. image:: https://github.com/sakuv2/agarilog/blob/main/img/telegram_sample.png?raw=true

Slack
#####

.. image:: https://github.com/sakuv2/agarilog/blob/main/img/slack_sample.png?raw=true

Chatwork
########

.. image:: https://github.com/sakuv2/agarilog/blob/main/img/chatwork_sample.png?raw=true

Environment
-----------

| 環境変数にサービスごとの設定を登録する。
| もしくは実行パスと同じ場所の :code:`.env` ファイルに記述する。
| importの方法を変えることで任意のファイルを読み込むこともできる。(上記参照)

**Environment variables will always take priority over values loaded from a dotenv file.**

Telegram
########

.. code-block::

    LOG_TELEGRAM_TOKEN=XXXXXXXXX:YYYYYYYYYYYYYYYYYYYYYYYYYYYY
    LOG_TELEGRAM_CHAT_ID=XXXXXXXX
    LOG_TELEGRAM_LEVEL=WARNING # default is warning

Slack
#####

.. code-block::

    LOG_SLACK_TOKEN=xxxx-YYYYYYYYYYYY-YYYYYYYYYYYY-xxxxxxxxxxxxxxxxxxxxx
    LOG_SLACK_CHANNEL=XXXXXXXXXXX
    LOG_SLACK_LEVEL=WARNING # default is warning

Chatwork
########

.. code-block::

    LOG_CHATWORK_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    LOG_CHATWORK_ROOM_ID=XXXXXXXXX
    LOG_CHATWORK_LEVLE=WARNING # default is warning


Development
-----------

| :code:`git clone` したら最初に実行すること。
| 仮想環境作成と :code:`pre-commit` のインストールが行われる。

.. code-block::

    $ make init
