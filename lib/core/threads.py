import threading
import time
from lib.core.log import ConsoleLogger,FileLogger
from lib.core.enums import LOGGING_MESSAGE
from lib.core.datatype import AttribDict
import requests
from bs4 import BeautifulSoup

class MyThread(threading.Thread):
    def __init__(self,realman,lock):
        threading.Thread.__init__(self)
        self.realman=realman
        self.lock=lock

    def run(self):
        while self.realman.queue.empty()==False:
            lock_flag=0#锁状态，0为解锁，1为上锁
            self.lock.acquire()
            lock_flag=1
            try:
                item=self.realman.queue.get()
                self.lock.release()
                lock_flag=0
                result=self.realman.obj.poc(item)
                if result:
                    ConsoleLogger.Info(LOGGING_MESSAGE.FOUND_MESSAGE.format(url=item))
                    self.lock.acquire()
                    lock_flag=1
                    exist=AttribDict()
                    exist.url=item
                    exist.result=result
                    self.realman.exist.append(exist)
            except Exception as e:
                pass
            finally:
                if lock_flag==1:
                    self.lock.release()

#对网站爬虫的多线程实现
class SpiderThread(threading.Thread):
    def __init__(self,queue,urlbugobj,domain,lock):
        threading.Thread.__init__(self)
        self.queue=queue
        self.urlbugobj=urlbugobj
        self.lock=lock
        self.domain=domain
        self.headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
    def run(self):
        while self.queue.empty()==False:
            lock_flag=0#锁状态，0为解锁，1为上锁
            self.lock.acquire()
            lock_flag=1
            try:
                item=self.queue.get(timeout=3)
                self.lock.release()
                lock_flag=0
                response=requests.get(item,headers=self.headers,verify=False,timeout=3)
                text=response.text
                self.lock.acquire()
                lock_flag=1
                self.urlbugobj.crawled.add(item)
                soup = BeautifulSoup(text,"lxml")
                for i in soup.find_all('link'):
                    self.urlbugobj.uncrawl.add(self.urlbugobj.repair_url(self.domain,i.get('href')))
                for j in soup.find_all('a'):
                    self.urlbugobj.uncrawl.add(self.urlbugobj.repair_url(self.domain,j.get('href')))
            except Exception as e:
                pass
            finally:
                if lock_flag==1:
                    self.lock.release()
                if self.queue.qsize()==0:
                    break

        
