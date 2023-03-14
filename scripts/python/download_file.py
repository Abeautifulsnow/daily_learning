import asyncio
import time
from typing import Any, AnyStr, List

import aiohttp


async def job(session: Any, url: AnyStr) -> AnyStr:
    name = url.split('/')[-1]
    img = await session.get(url)
    imgcode = await img.read()

    local_url = "/Users/dapeng/Desktop/ps-materail/" + str(name)
    with open(local_url, 'wb') as f:
        f.write(imgcode)
    
    return url, local_url


async def main(loop: Any, URL: List[AnyStr]):
    async with aiohttp.ClientSession() as session:
        tasks = [loop.create_task(job(session, URL[_])) for _ in range(2)]
        done, pending = await asyncio.wait(tasks)

        all_results_origin_url = [r.result()[0] for r in done]
        all_results_local_url = [r.result()[1] for r in done]

        print('ALL RESULTS: '
        f'\norigin-url:{all_results_origin_url}'
        f'\n\nlocal-url:{all_results_local_url}')


t_start = time.time()
URLS = [
    'https://pythondict.com/wp-content/uploads/2020/08/2020080318025478.png',
    'https://imagesvc.meredithcorp.io/v3/mm/image?url=https://static.onecms.io/wp-content/uploads/sites/9/2017/05/red-pandas-2-FT-BLOG0517.jpg'
]
loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop, URLS))
loop.close()
t_end = time.time()
print(f'Total time cost: {t_end - t_start}(s) elapsed.')
