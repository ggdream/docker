import os
import re
import json
import time
import requests
import asyncio
import logging
from ffmpy3 import FFmpeg
from aiohttp import request



logging.basicConfig(
    level=logging.DEBUG,
    filename='/data/down.log',
    filemode='a',
    format='%(asctime)s --     %(message)s'
)


class GetUrl:
    def __init__(self, bvid: str):
        self.bvid = bvid
        self.__url1 = f"https://www.bilibili.com/video/{bvid}"
        self.__url2 = f"https://www.bilibili.com/video/{bvid}?p=%d"

        self.__headers = {
            "referer": self.__url1,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
        }
        self.number, self.pages = self.__parsefirst()

    @staticmethod
    def getpage(data: str) -> dict:
        res = re.findall('window.__INITIAL_STATE__=(.*?);\(function', data)[0]
        return json.loads(res)

    @staticmethod
    def getplay(data: str) -> dict:
        res = re.findall('window.__playinfo__=(.*?)</script>', data)[0]
        return json.loads(res)

    def __parsefirst(self) -> tuple:
        data = requests.get(self.__url1, self.__headers).content.decode()
        page_page = self.getpage(data)
        return page_page["videoData"]["videos"], page_page["videoData"]["pages"]

    async def grab(self, num: int, maps: dict):
        async with request('GET', self.__url2 % num, headers=self.__headers) as res:
            data = await res.text()
            dash = self.getplay(data)["data"]["dash"]
            print(json.dumps(dash))
            maps[str(num)] = {
                "video": dash["video"][0]["baseUrl"],
                "audio": dash["audio"][-1]["baseUrl"],
                "title": self.pages[num - 1]["part"]
            }

    async def fetch(self, maps: dict):
        tasks = [self.grab(i + 1, maps) for i in range(self.number)]
        await asyncio.wait(tasks)
        await asyncio.sleep(10)


class Download:
    def __init__(self, bv: str, path: str, maps: dict):
        self.maps = maps
        self.path = path

        self.__headers = {
            "range": "bytes=0-",
            "referer": f"https://www.bilibili.com/video/{bv}",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
        }

    async def __down(self, num: str, dash: dict, isVideo: bool):
        async with request('GET', dash["video"] if isVideo else dash["audio"], headers=self.__headers) as res:
            with open(f'{self.path}/{num}.{"mp4" if isVideo else "mp3"}', 'wb') as f:
                while True:
                    chunk = await res.content.read(1 << 10)
                    if not chunk:
                        break
                    f.write(chunk)

    async def downs(self, num: str, semaphore: asyncio.Semaphore):
        async with semaphore:
            dash = self.maps[num]

            logging.info(f'video ->{dash["title"]}')
            await self.__down(num, dash, True)

            logging.info(f'video <-{dash["title"]}')

            logging.info(f'audeo ->{dash["title"]}')
            await self.__down(num, dash, False)
            logging.info(f'audeo <-{dash["title"]}')

    async def fetch(self, semNumber: int):
        semaphore = asyncio.Semaphore(semNumber)
        tasks = [self.downs(i, semaphore) for i in self.maps.keys()]
        await asyncio.wait(tasks)
        await asyncio.sleep(1 << 3)


class Merge:
    def __init__(self, path: str, src_path: str, maps: dict):
        self.maps = maps
        self.path = path
        self.src_path = src_path

        if not os.path.exists(f'{self.path}/dst'):
            os.makedirs(f'{self.path}/dst')

    def merge(self, num: str):
        logging.info(f'merge ->{self.maps[num]["title"]}')
        ff = FFmpeg(
            inputs={
                f'{self.src_path}/{num}.mp4': None,
                f'{self.src_path}/{num}.mp3': None,
            },
            outputs={
                f'{self.path}/dst/{self.maps[num]["title"]}.mp4': '-c:v copy -c:a copy'
            },
            global_options=['-loglevel quiet']
        )
        ff.run()
        logging.info(f'merge <-{self.maps[num]["title"]}')


def help(v: str) -> str:
    if v == "--help":
        import sys
        print('\n--------------------------------------------')
        print("$ docker run -d -v <storage path>:/data ggdream/bilibili <BV>")
        print('--------------------------------------------\n\n')
        sys.exit(0)
    
    return v



if __name__ == '__main__':
    import sys
    from multiprocessing import cpu_count

    bvid = help(sys.argv[1])
    path = "/data"
    src_path = "/tmp"
    semaphores = 1 << 3
    processes = cpu_count()

    av_urls_map = {}
    g = GetUrl(bvid)
    asyncio.run(g.fetch(av_urls_map))

    with open(f'{path}/map.json', 'a') as f:
        json.dump(av_urls_map, f, ensure_ascii=False)

    d = Download(bvid, src_path, av_urls_map)
    asyncio.run(d.fetch(semaphores))

    try:
        from concurrent.futures.process import ProcessPoolExecutor      # version >= 3.8
    except ImportError:
        from concurrent.futures import ProcessPoolExecutor              # version < 3.8

    m = Merge(path, src_path, av_urls_map)
    with ProcessPoolExecutor(max_workers=processes) as pool:
        for num in av_urls_map.keys():
            pool.submit(m.merge, num)
