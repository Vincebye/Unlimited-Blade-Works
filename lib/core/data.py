from lib.core.datatype import AttribDict
from configparser import ConfigParser
import queue

headers={
     'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
     'Connection': 'close'
     }
cfg=ConfigParser()
cfg.read('lib/core/config.ini')
#作为所有路径传参
paths=AttribDict()
#存储命令相关参数
conf=AttribDict()
##存储其他信息的一个全程对象
realman=AttribDict()
#存储目标的一个队列
realman.queue=queue.Queue()
#存储目标的一个list
realman.tlist=[]
#存储收集信息的一个dict
realman.timo=AttribDict()
#存储payload验证存在漏洞地址的url的list
realman.exist=[]
