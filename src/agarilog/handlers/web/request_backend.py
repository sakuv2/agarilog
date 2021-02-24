"""メインスレッドとは違うところでQueueにたまったリクエストを送り続けるバックエンド機構
"""
import asyncio
import threading
from queue import Queue
from typing import Dict, List, Optional, Tuple, Union

import aiohttp
from pydantic import BaseModel, HttpUrl, validator

from ._helper import is_ipython, to_thread


class Request(BaseModel):
    """Requestするためのデータセット

    Args:
        method (Literal["GET", "POST"]): HTTPメソッド
        url (HttpUrl): URL
        headers (Dict[str, str]): ヘッダー
        data (Optional[bytes]): データ
        json_ (Optional[dict]): jsonを送るときはこっち
        params (Optional[Union[List[Tuple[str, str]], Dict[str, str]]]): query string
    """

    method: str
    url: HttpUrl
    headers: Dict[str, str]
    data: Optional[Union[dict, bytes]]
    json_: Optional[dict]
    params: Optional[Union[List[Tuple[str, str]], Dict[str, str]]]

    @validator("method")
    def _valid_method(cls, v):
        if v not in ["GET", "POST"]:
            raise ValueError('method is "GET" or "POST"')
        return v


class RequestBackend:
    def __init__(self, limit=10) -> None:
        self.is_ipython = is_ipython()
        self.queue: Queue[Optional[Request]] = Queue()
        self.thread = self._start_new_thread()
        self.limit = limit

        # ipython起動の場合セルの開始と終了でスレッドを再作成&停止するようにする
        if self.is_ipython:
            ip = eval("get_ipython()")
            ip.events.register("pre_execute", self.restart)
            ip.events.register("post_execute", self.shutdown)

    def post(
        self,
        url: str,
        params: Optional[Union[List[Tuple[str, str]], Dict[str, str]]] = None,
        data: Optional[Union[dict, bytes]] = None,
        json: Optional[dict] = None,
        headers: Dict[str, str] = {},
    ):
        request = Request(
            method="POST", url=url, params=params, data=data, json_=json, headers=headers
        )
        self._put(request)

    def get(
        self,
        url: str,
        params: Optional[Union[List[Tuple[str, str]], Dict[str, str]]] = None,
        headers: Dict[str, str] = {},
    ):
        request = Request(method="GET", url=url, params=params, headers=headers)
        self._put(request)

    def restart(self):
        if self.thread is not None and self.thread.is_alive():
            return
        # スレッドが初期化されていないまたはスレッドが死んでいるならば新しいスレッドを起動する
        self.thread = self._start_new_thread()

    def shutdown(self):
        if self.thread is None or not self.thread.is_alive():
            return
        self._put(None)  # 終了命令を通知
        self.thread.join()

    def _start_new_thread(self) -> threading.Thread:
        th = threading.Thread(target=asyncio.run, args=[self._worker()])
        th.start()
        return th

    def _put(self, item: Union[Request, str]):
        self.queue.put_nowait(item)

    async def _send_request(
        self, session: aiohttp.ClientSession, request: Request, semaphore: asyncio.Semaphore
    ):
        method = self._get if request.method == "GET" else self._post
        async with semaphore:
            await method(session, request)

    @staticmethod
    async def _get(sess: aiohttp.ClientSession, r: Request):
        obj = dict(url=r.url, params=r.params, headers=r.headers)
        async with sess.get(**obj) as res:
            res.raise_for_status()

    @staticmethod
    async def _post(sess: aiohttp.ClientSession, r: Request):
        obj = dict(url=str(r.url), params=r.params, data=r.data, json=r.json_, headers=r.headers)
        async with sess.post(**obj) as res:
            res.raise_for_status()

    async def _worker(self) -> bool:
        """QueueにたまったRequestを処理する奴

        Returns:
            bool: 完了したらTrueを返す
        """

        # ipython起動じゃなければmainスレッド終了時に終了を通知する機構を仕込む
        if not self.is_ipython:
            asyncio.create_task(self._wait_main_thread())

        sem = asyncio.Semaphore(self.limit)

        async with aiohttp.ClientSession() as session:
            tasks = []
            while True:
                request: Request = await to_thread(self.queue.get)
                if request is None:
                    break
                send_request = self._send_request(session, request, sem)
                tasks.append(asyncio.create_task(send_request))
                tasks = [task for task in tasks if not task.done()]
            if tasks != []:
                await asyncio.wait(tasks)
        return True

    async def _wait_main_thread(self):
        """メインスレッドの停止を確認したらqueueにNone(停止命令)をいれる"""
        main = threading.main_thread()
        await to_thread(main.join)
        self._put(None)
