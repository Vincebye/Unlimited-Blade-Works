from lib.core.data import *
from lib.core.zoomeye import ZoomEye
def get_targets():
    if conf.url:
        realman.queue.put(conf.url)
    elif conf.list:
        for i in open(conf.list,'r').readlines():
            realman.queue.put(i)
    elif conf.zoomeye:
        for i in zoomeye_api(conf.keyword,conf.limitnum):
            realman.queue.put(i)

def zoomeye_api(query,num):
    zoom=ZoomEye()
    return zoom.query(query,num)

