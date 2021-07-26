import requests, os, time
import aiohttp, asyncio


class Spider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        self.num = 1

        storage_path = '/Users/dapeng/Desktop/ps-materail/'
        album_path = os.path.join(storage_path, 'album')
        if 'album' not in os.listdir(storage_path):
            os.mkdir(album_path)

        self.path = album_path
        os.chdir(self.path)  # 进入文件下载路径

    async def __get_content(self, link):
        async with aiohttp.ClientSession() as session:
            response = await session.get(link)
            content = await response.read()
            return content

    def __get_img_links(self, page):
        url = 'https://unsplash.com/napi/photos'
        data = {
            'page': page,
            'per_page': 12,
            'order_by': 'latest'
        }
        response = requests.get(url, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            print('请求失败，状态码为%s' % response.status_code)

    async def __download_img(self, img):
        content = await self.__get_content(img[1])
        with open(img[0]+'.jpg', 'wb') as f:
            f.write(content)
        print('下载第%s张图片成功' % self.num)
        self.num += 1

    def run(self):
        start = time.time()
        for x in range(1, 101):  # 下载一百页的图片就可以了，或者自己更改页数
            links = self.__get_img_links(x)
            tasks = [asyncio.ensure_future(self.__download_img((link['id'], link['links']['download']))) for link in links]
            print(f'tasks: {tasks}')
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
            if self.num >= 10:  # 测试速度使用，如需要下载多张图片可以注释这段代码
               break
        end = time.time()
        print('共运行了%s秒' % (end - start))

def main():
    spider = Spider()
    spider.run()


if __name__ == '__main__':
    main()
