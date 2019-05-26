from lib.core.data import *
from lib.core.output import output
from lib.core.threads import MyThread
from lib.core.log import ConsoleLogger,FileLogger
import threading
from multiprocessing import Pool,Manager
import asyncio
import async_timeout
import aiohttp
import threading
from lib.core.enums import LOGGING_MESSAGE
def run():
    ConsoleLogger.Info(LOGGING_MESSAGE.START_SCAN_MESSAGE)
    scan()

def processing_work(list1,item):
    result=realman.obj.poc(item)
    per=AttribDict()
    if result:
        per.url=item
        per.result=result
        list1.append(per)
async def async_work(item):
    try:
        with async_timeout.timeout(8):
            status=await realman.obj.poc(item)
            if status:
                realman.exist.append(item)
    except Exception as e:
        print(e)


def scan():
    if conf.mode=='eT':
        ConsoleLogger.Warning(LOGGING_MESSAGE.RUNNING_MODE_ET)
        ConsoleLogger.Warning(LOGGING_MESSAGE.THREAD_NUM.format(number=conf.thread))
        threads=[]
        threadLock = threading.Lock()
        for i in range(int(conf.thread)):
            thread1 = MyThread(realman,threadLock)
            thread1.start()
            threads.append(thread1)
        for t in threads:
            t.join()

    elif conf.mode=='eP':
        ConsoleLogger.Warning(LOGGING_MESSAGE.RUNNING_MODE_EP)
        ConsoleLogger.Warning(LOGGING_MESSAGE.PROCESS_NUM.format(number=4))
        manager=Manager()
        list1=manager.list()
        p = Pool(4)
        for i in range(500):
            if realman.queue.empty()==False:
                item=realman.queue.get().strip("\n")  
                p.apply_async(processing_work,args=(list1,item))
            else:
                break
        p.close()
        p.join()
        realman.exist.extend(list1)
    elif conf.mode=='eC':
        ConsoleLogger.Warning(LOGGING_MESSAGE.RUNNING_MODE_EC)

        #定义一个新的request方法，根据参数值决定是同步还是异步请求方法
        tasks=[asyncio.ensure_future(async_work(str(i))) for i in realman.tlist]
        loop=asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
    else:
        while realman.queue.empty()==False:
            item=realman.queue.get()
            if(realman.queue.qsize()):
                break
            if isinstance(item,str):
                item=realman.queue.get().strip("\n")
            if conf.script:
                result=realman.obj.poc(item)
                if result:
                    exist=AttribDict()
                    exist.url=item
                    exist.result=result
                    realman.exist.append(exist)
    ConsoleLogger.Info(LOGGING_MESSAGE.END_SCAN_MESSAGE)
    ConsoleLogger.Info(LOGGING_MESSAGE.OUTPUT_SCAN_MESSAGE)
    output(realman,conf)
