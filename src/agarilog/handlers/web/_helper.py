import asyncio
from concurrent.futures import ThreadPoolExecutor


def is_ipython() -> bool:
    try:
        eval("get_ipython()")
    except NameError:
        return False
    return True


async def to_thread(func, *args, **kwargs):
    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_running_loop()
        coro = loop.run_in_executor(executor, func, *args, **kwargs)
        return await coro
