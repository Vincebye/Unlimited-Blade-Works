# -*- coding: utf-8 -*- 
import requests
import re
import urllib3
from bs4 import BeautifulSoup
from lxml import etree
import time
urllib3.disable_warnings()
import asyncio
import async_timeout
import aiohttp


class BaiduApi():
    def __init__(self,keyword,num=20):
        self.keyword=keyword
        self.num=num
        self.headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        self.result=[]
    
    def search(self):
        url_list=[]
        page=self.num//10
        for per in range(page):
            baiduurl='https://www.baidu.com/s?wd='+str(self.keyword)+'&pn='+str(per*10)
            text=requests.get(baiduurl,headers=self.headers,verify=False).text
            url_list.extend(re.findall('<h3[\s\S]*?<a[^>]*?href[^>]*?"(.*?)"[^>]*?>(.*?)</a>',text))
        url_result=[]
        for i in url_list:
            url_result.append(i[0])
        return url_result

    async def fetch(self,url):
        try:
            with async_timeout.timeout(8):
                async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:  
                        async with session.get(url) as response:
                            #assert response.status == 200
                            url=response.url
                            self.result.append(url)
                            return url
        except Exception as e:
            print(e)
    def run(self):
        urllist=self.search()
        tasks=[asyncio.ensure_future(self.fetch(i)) for i in urllist]
        loop=asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        # for i in self.result:
        #     print(i)
        return self.result
# a=BaiduApi("美女",30)
# a.run()