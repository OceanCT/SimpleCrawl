import threading

from crawler import Crawler
from public.logger import Logger
from public.pool import Pool
import queue
from concurrent.futures import ThreadPoolExecutor


# 防止queue无限增长耗尽内存,自定义类
class MaxSizeThreadPollExecutor(ThreadPoolExecutor):
    def __init__(self, *args, **kwargs):
        super(MaxSizeThreadPollExecutor, self).__init__(*args, **kwargs)
        self._work_queue = queue.Queue(3)


class Starter:
    def __init__(self, max_threads):
        self.logger = Logger("crawl.log")
        self.logger.log("Starting crawling")
        self.proxy_pool = Pool(max_size=10)
        self.url_pool = Pool(max_size=100)
        self.crawler = Crawler()
        self.executor = MaxSizeThreadPollExecutor(max_workers=max_threads)

    def start(self):
        threading.Thread(target=self.add_proxy).start()
        threading.Thread(target=self.add_url).start()
        while True:
            self.crawl_once()

    def add_proxy(self):
        self.proxy_pool.put(self.crawler.get_proxy())

    def add_url(self):
        self.url_pool.put(self.crawler.get_url())

    def crawl_once(self) -> True:
        proxy = self.proxy_pool.get()
        if not proxy:
            self.logger.log("No proxy available")
            return False
        url = self.url_pool.get()
        if not url:
            self.logger.log("No url available")
            self.proxy_pool.put(proxy)
            return False
        self.logger.log("Crawling url: %s by proxy: %s" % (url, proxy))
        self.executor.submit(self.crawler.crawl, proxy, url)
        return True

    def stop(self):
        self.logger.log("Crawling stopped")
        self.logger.close()
        self.crawler.close()
        return True

    def __del__(self):
        self.stop()
