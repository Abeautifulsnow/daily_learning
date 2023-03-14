import asyncio
import re
import time
from typing import IO, Callable, Dict, List

import aiofiles
import httpx
import requests
import urllib3

urllib3.disable_warnings()

# m3u8_path = "https://13.cdn-vod.huaweicloud.com/asset/94a33fb7bb3c6c6b514d7463f4be98ce/play_video/442d776c312aa0b57193ae1deae9f943/cb8db232c9e31a09c25df076c5f71a4d_2.m3u8"
m3u8_path = 'https://13.cdn-vod.huaweicloud.com/asset/e0a13b1737c48e6335b760a3dffaf4cf/play_video/7d5c1d3316918cd9484941c2b468a44e.m3u8'
header = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.20 Safari/537.36"
}


def applyUrl(target_url: str, base_url: str) -> str:
    if 'http' in target_url:
        return target_url

    if target_url[0] == '/':
        base_url_list = base_url.split('/')
        return base_url_list[0] + '//' + base_url_list[2] + target_url

    base_url_list = base_url.split('/')
    base_url_list.pop()
    return '/'.join(base_url_list) + '/' + target_url


async def get_ts_lists(m3u8_path: str) -> List[str]:
    ts_urls: List[str] = []
    print("正在解析：" + m3u8_path.split("/")[-1])
    async with httpx.AsyncClient(headers=header, verify=False) as client:
        res = await client.get(url=m3u8_path)
        r = await res.aread()
        # 通过正值表达式获取key和ts的链接
        k = re.compile(r'(.*URI="([^"]+))"')
        t = re.compile(r".*?.ts")
        iv = re.compile(r'(.*IV=([^,\s]+))')
        key_url_list = k.findall(r.decode(encoding='utf-8'))
        key_url = key_url_list[0][1] if len(key_url_list) != 0 else ''
        iv_s_list = iv.findall(r.decode(encoding='utf-8'))
        iv_s = iv_s_list[0][1] if len(iv_s_list) != 0 else ''
        ts_urls = t.findall(r.decode(encoding='utf-8'))

    if len(ts_urls) != 0:
        for idx, ts_url in enumerate(ts_urls):
            ts_url = applyUrl(ts_url, m3u8_path)
            ts_urls[idx] = ts_url

    return ts_urls


async def download_m3u8_file(ts_url: str) -> Dict[str, httpx.Response]:
    res_dict: Dict[str, httpx.Response] = {}
    ts_name = ts_url.split("/")[-1]
    print("正在下载：" + ts_name)

    async with httpx.AsyncClient(headers=header, verify=False) as client:
        res = await client.get(ts_url)
        res_dict.setdefault(ts_name, res)

    return res_dict


def write_to_file(file: IO, res: Dict[str, httpx.Response]):
    item = res.popitem()
    ts_name, te_res = item[0], item[1]
    file.write(te_res.read())
    print("保存成功：" + ts_name)


async def down_main(ts_urls: List[str]) -> List[Dict[str, httpx.Response]]:
    return_res = await asyncio.gather(
        *[download_m3u8_file(ts_url) for ts_url in ts_urls])
    return return_res


def write_file(file_name: str, func: Callable[IO, Dict[str, httpx.Response]],
               down_res: List[Dict[str, httpx.Response]]):
    with open(file_name, 'ab') as file:
        for res in down_res:
            func(file, res)


if __name__ == '__main__':
    name = "./dream_it_possible.ts"
    mutex = asyncio.Lock()
    ts_urls = asyncio.run(get_ts_lists(m3u8_path))
    return_res = asyncio.run(down_main(ts_urls))
    write_file(name, write_to_file, return_res)
    print(name, "下载完成")
