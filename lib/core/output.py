from lib.core.data import *
from prettytable import PrettyTable
from lib.core.log import ConsoleLogger,FileLogger
import os
NowPath=os.path.abspath(os.path.dirname(__file__))
ScriptPath=NowPath+'/../../script/'

def clear_output():
    return [i.strip('\n') for i in realman.exist]
        
def output(realman,conf):
    if conf.url:
        table=PrettyTable(['ID','Poc','Url','Result','CMSName'])
    else:
        table=PrettyTable(['ID','Poc','Url','Result'])
    id=1
    if conf.url:
        for i in realman.exist:
            table.add_row([id,conf.script,i.url,i.result,realman.timo.cms])
            id=id+1
    else:
        for i in realman.exist:
            table.add_row([id,conf.script,i.url,i.result])
            id=id+1
    if conf.url or conf.list or conf.baidu or conf.zoomeye or conf.spider:
        if len(realman.exist)!=0:
            print(table)
    
    id=1
    if conf.showscript:
        table=PrettyTable(['ID','Poc','Product','Vultype'])
        for i in os.listdir(ScriptPath):
            try:
                table.add_row([id,i.split('.')[0],i.split('_')[0],i.split('_')[-1].split('.')[0]])
            except:
                table.add_row([id,i,'Unknow','Unknow'])

            id=id+1
        print(table)