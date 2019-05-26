from lib.core.data import *
from lib.core.zoomeye import ZoomEye
from lib.core.baidu import BaiduApi
from lib.core.spider import Urlspider
from lib.core.log import ConsoleLogger,FileLogger
from lib.core.enums import LOGGING_MESSAGE
from netaddr import *
import re
def get_targets():
    if conf.url:
        segment=ipsegment(conf.url)
        if segment:
            for i in segment:
                realman.queue.put(i)
                realman.tlist.append(i)
        else:
            ConsoleLogger.Info(LOGGING_MESSAGE.GATHER_TYPE_URL)
            realman.queue.put(conf.url)
            realman.tlist.append(conf.url)
    elif conf.list:
        ConsoleLogger.Info(LOGGING_MESSAGE.GATHER_TYPE_LIST)
        for i in open(conf.list,'r').readlines():
            realman.queue.put(i.strip('\n'))
            realman.tlist.append(i.strip('\n'))
    elif conf.baidu:
        ConsoleLogger.Info(LOGGING_MESSAGE.GATHER_TYPE_BAIDU)
        for i in baidu_search(conf.baidu,conf.limitnum):
            realman.queue.put(i)
            realman.tlist.append(i)
    elif conf.zoomeye:
        ConsoleLogger.Info(LOGGING_MESSAGE.GATHER_TYPE_ZOOMEYE)
        for i in zoomeye_api(conf.zoomeye,conf.limitnum):
            realman.queue.put(i)
            realman.tlist.append(i)
    elif conf.spider:
        ConsoleLogger.Info(LOGGING_MESSAGE.GATHER_TYPE_SPIDER)
        for i in urlspider(conf.spider,conf.deepth):
            realman.queue.put(i)
            realman.tlist.append(i)
    
def zoomeye_api(query,num):
    zoom=ZoomEye(query,num)
    return zoom.query()
def baidu_search(query,num):
    baidu=BaiduApi(query,num)
    return baidu.run()

def urlspider(query,deepth):
    spider=Urlspider(query,deepth)
    return spider.run()

def ipsegment(url):
    if '*' in url:
        return [url.replace('*',str(i)) for i in range(255)]
    elif re.search(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2}',url):
        ip = IPNetwork(url)
        ip_list = list(ip)
        return [i for i in ip_list]
    elif re.search(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}-[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',url):
        url_list=[]
        ip_start=url.split('-')[0].split('.')[-1]
        ip_end=url.split('.')[-1]
        ip_seg=url.split('.')[0:3]
        for i in range(int(ip_start),int(ip_end)+1):
            temp=url.split('.')[0:3]
            temp.append(str(i))
            url_list.append('.'.join(temp))
        return url_list

