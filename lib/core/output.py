from lib.core.data import *
from prettytable import PrettyTable

table=PrettyTable(['Poc','IP'])

def clear_output():
    return [i.strip('\n') for i in realman.exist]
        
def output():
    for i in clear_output():
        table.add_row([conf.script,i])
    print(table)