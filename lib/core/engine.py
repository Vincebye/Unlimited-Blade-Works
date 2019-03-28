from lib.core.data import *
from lib.core.output import output
import threading
from multiprocessing import Pool,Manager
import asyncio
import async_timeout
import aiohttp
def run():
    scan()


def threading_work():
    if realman.queue.empty()==False:
        item=realman.queue.get()
        if realman.obj.poc(item):
            realman.exist.append(item)

def processing_work(list1,item):
    # if realman.queue.empty()==False:
    #     item=realman.queue.get()
    #     print('***********')
    #     print(item)
    if realman.obj.poc(item):
        list1.append(item)
            #realman.exist.put(item)
            #realman.exist.extend(temp)
async def async_work(url):
    try:
        with async_timeout.timeout(8):
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                response=await session.get(url)
                assert response.status==200
                text=await response.read()
                await session.close()
    except Exception as e:
        print(e)


def scan():
    if conf.mode=='eT':
        threads=[]
        for i in range(int(conf.thread)):
            thread=threading.Thread(target=threading_work)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
    elif conf.mode=='eP':
        manager=Manager()
        list1=manager.list()
        p = Pool(4)
        for i in range(5):
            if realman.queue.empty()==False:
                item=realman.queue.get()
                p.apply_async(processing_work,args=(list1,item))
            else:
                break
        p.close()
        p.join()
        realman.exist.extend(list1)
    elif conf.mode=='eC':
        #定义一个新的request方法，根据参数值决定是同步还是异步请求方法
        tasks=[asyncio.ensure_future(async_work(str(i))) for i in realman.tlist]
        loop=asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

    output()
    print('end')
