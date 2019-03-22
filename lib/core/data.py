from lib.core.datatype import AttribDict
from configparser import ConfigParser
import queue

cfg=ConfigParser()
cfg.read('lib/core/config.ini')
#作为所有路径传参
paths=AttribDict()
#存储命令相关参数
conf=AttribDict()
##存储其他信息的一个全程对象
realman=AttribDict()
realman.queue=queue.Queue()