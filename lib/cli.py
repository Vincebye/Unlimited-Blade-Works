from lib.core.common import set_paths
from lib.parse.cmdline import cmdline_parse
from lib.core.data import *
from lib.core.loader import load_module,load_payload
from lib.core.engine import *
from lib.core.log import SetLogger
from lib.core.common import banner

def main():
    #设置相关路径绝对变量，相当于一些变量从配置文件读取进行初始化
    set_paths()
    #从终端命令获取输入参数，并更新给一个变量
    conf.update(cmdline_parse().__dict__)

    
#    get_cmd()

    #初始化日志设置
    SetLogger()
    #程序运行后显示的banner图案
    banner()
    #从script文件夹中读取的module对象
    load_module()
    #获取攻击目标
    load_payload()
    #开始运行程序
    run()
