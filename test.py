import asyncio
import aiohttp
import time


async def request_web(i: int):
    print(f'Number: {i}')
    async with aiohttp.ClientSession() as session:
        async with session.get("https://baidu.com"):
            pass


def main():
    loop = asyncio.get_event_loop()

    tasks = []
    for i in range(10):
        tasks.append(request_web(i))
    t_s = time.time()
    loop.run_until_complete(asyncio.wait(tasks))
    t_e = time.time()
    print(f"Spend time: {(t_e - t_s) * 1000} ms")


main()
