import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .request_backend import RequestBackend

try:
    ip = eval("get_ipython()")

    def register(rb: "RequestBackend"):
        """Decorator that registers at post_execute. After its execution it
        unregisters itself for subsequent runs."""

        ip.events.register("pre_execute", rb.init)
        ip.events.register("post_execute", rb.shutdown)


except NameError:
    import atexit

    def register(rb: "RequestBackend"):
        rb.init()
        atexit.register(rb.shutdown)


async def to_thread(func, *args, **kwargs):
    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_running_loop()
        coro = loop.run_in_executor(executor, func, *args, **kwargs)
        return await coro
