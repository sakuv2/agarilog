"""メインスレッドとは違うところでQueueにたまったリクエストを送り続けるバックエンド機構
"""
import asyncio
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from typing import Dict, List, Optional, Tuple, Union

import aiohttp
from pydantic import BaseModel, HttpUrl, validator

from ._helper import register, to_thread


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
    def __init__(self) -> None:
        self.flg_init = False
        register(self)  # 待機する処理を加える(IPythonと通常実行で処理を切り替える)

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

    def init(self):
        if self.flg_init:
            return
        self.queue: Queue[Union[Request], str] = Queue()
        self.executor = ThreadPoolExecutor()
        self.future = self.executor.submit(asyncio.run, self._worker())
        self.flg_init = True

    def shutdown(self):
        if not self.flg_init:
            return
        self._put("STOP")
        self.future.result()
        self.executor.shutdown()
        self.flg_init = False

    def _put(self, item: Union[Request, str]):
        self.queue.put_nowait(item)

    async def _send_request(self, session: aiohttp.ClientSession, request: Request):
        method = self._get if request.method == "GET" else self._post
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
        async with aiohttp.ClientSession() as session:
            tasks = []
            while True:
                request = await to_thread(self.queue.get)
                if request == "STOP":
                    break
                send_request = self._send_request(session, request)
                tasks.append(asyncio.create_task(send_request))
                tasks = [task for task in tasks if not task.done()]
            if len(tasks) != 0:
                await asyncio.wait(tasks)
        return True
