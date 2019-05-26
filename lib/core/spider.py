import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse,urljoin
import urllib3
import os
import time
import aiohttp
import asyncio
import async_timeout
from lib.core.data import conf
from lib.core.log import ConsoleLogger,FileLogger
from lib.core.enums import LOGGING_MESSAGE
import queue
urllib3.disable_warnings()
class Urlspider(object):
    def __init__(self,target,deepth):
        self.uncrawl=set()#待爬取
        self.crawled=set()#爬取了
        self.mail=set()
        self.url=target
        self.deepth=deepth
        self.headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        self.static_suffix=['ico','js','css','jpg','png']

    #首次爬取URL，获取页面其他URL
    def crawl_url(self):
        try:
            text=requests.get(self.url,headers=self.headers,verify=False,timeout=7).text
        except Exception as e:
            #print(self.url)
            #print(e)
            return False
        # domain=urlparse(url).scheme+'://'+urlparse(url).netloc
        #print(self.url)
        self.crawled.add(self.url)
        soup = BeautifulSoup(text,"lxml")
        for i in soup.find_all('link'):
            self.uncrawl.add(self.repair_url(self.url,i.get('href')))
        for j in soup.find_all('a'):
            self.uncrawl.add(self.repair_url(self.url,j.get('href')))
        return text
    def repair_url(self,domain,url):
        if url is None:
            url=''
        elif not url:
            url=''
        elif url.split('.')[-1] in self.static_suffix:
            url=domain+url
            self.crawled.add(url)
            url=''
        elif url[0]=='j' or url[0]=='J':
            url=''
        elif url.startswith('mail'):
            self.mail.add(url)
            url=''
        elif not url.startswith('http'):
            url=urljoin(domain,url)
        return url
    def generaliz_url(self,url):
        pass
    
    #爬取uncrawl中的所有URL
    def crawl_uncrawl(self):
        while len(self.uncrawl)!=0:
            self.uncrawl=self.uncrawl-self.crawled
            # self.crawling=self.uncrawl
            url=[]
            for i in self.uncrawl:
                if i:
                    url.append(i)
            for i in url:
                self.crawl_url(i)
    #显示所有已爬取链接
    def show_crawled(self):
        for i in self.crawled:
            print(i)
    async def fetch(self,url):
        sem = asyncio.Semaphore(100)
        try:
            async with sem:
                with async_timeout.timeout(10):
                    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                        response=await session.get(url)
                        assert response.status == 200
                        text=await response.read()
                        self.crawled.add(url)
                        soup = BeautifulSoup(text,"lxml")
                        for i in soup.find_all('link'):
                            self.uncrawl.add(self.repair_url(url,i.get('href')))
                        for j in soup.find_all('a'):
                            self.uncrawl.add(self.repair_url(url,j.get('href')))
                        await session.close()
        except Exception as e:
            pass

    def run(self):
        ConsoleLogger.Info(LOGGING_MESSAGE.SPIDER_SEED_URL.format(url=self.url))
        test=Urlspider(self.url,self.deepth)
        st=time.time()

        if test.crawl_url():
            while(self.deepth!=0):
                ConsoleLogger.Info(LOGGING_MESSAGE.SPIDER_DEEP_MESSAGE.format(deepth=self.deepth))
                test.uncrawl=test.uncrawl-test.crawled
                url=[]
                for i in test.uncrawl:
                    if i:
                        url.append(i)
                tasks=[asyncio.ensure_future(test.fetch(i)) for i in url]
                loop=asyncio.get_event_loop()
                loop.run_until_complete(asyncio.wait(tasks))
                ConsoleLogger.Info(LOGGING_MESSAGE.SPIDER_CRAWLED_NUMBER.format(number=len(test.crawled)))
                self.deepth=self.deepth-1
            end=time.time()
            #test.show_crawled()
            ConsoleLogger.Info(LOGGING_MESSAGE.SPIDER_COST_TIME.format(seconds=(end-st)))
            return test.crawled
        else:
            ConsoleLogger.Info(LOGGING_MESSAGE.SPIDER_IP_FORBIDDEN)

    #多线程太慢了，遂放弃，寻另一解决方案
    def run_by_thread(self):
        import threading
        from lib.core.threads import SpiderThread

        ConsoleLogger.Info(LOGGING_MESSAGE.SPIDER_SEED_URL.format(url=self.url))
        test=Urlspider(self.url,self.deepth)
        st=time.time()
        if test.crawl_url():
            while(self.deepth!=0):
                ConsoleLogger.Info(LOGGING_MESSAGE.SPIDER_DEEP_MESSAGE.format(deepth=self.deepth))
                test.uncrawl=test.uncrawl-test.crawled
                uncrawled_queue=queue.Queue()

                for i in test.uncrawl:
                    if i:
                        uncrawled_queue.put(i)  
                threads=[]
                threadLock = threading.Lock()
                for i in range(int(conf.thread)):
                    thread1 = SpiderThread(uncrawled_queue,test,self.url,threadLock)
                    thread1.start()
                    threads.append(thread1)
                for t in threads:
                    t.join()
                ConsoleLogger.Info(LOGGING_MESSAGE.SPIDER_CRAWLED_NUMBER.format(number=len(test.crawled)))
                self.deepth=self.deepth-1
            end=time.time()
            ConsoleLogger.Info(LOGGING_MESSAGE.SPIDER_COST_TIME.format(seconds=(end-st)))

            return self.crawled
        else:
            ConsoleLogger.Info(LOGGING_MESSAGE.SPIDER_IP_FORBIDDEN)

