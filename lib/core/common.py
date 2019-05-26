from lib.core.data import paths
from lib.core.log import ConsoleLogger
import os
def set_paths():
    root_path=os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    paths.root=root_path
    paths.script=root_path+'/script'


def banner():
    logo='''
                                    
    //   / / //   ) ) ||   / |  / / 
   //   / / //___/ /  ||  /  | / /  
  //   / / / __  (    || / /||/ /   
 //   / / //    ) )   ||/ / |  /        author: {0}    version: {1}
((___/ / //____/ /    |  /  | /         update time: {2} scripts number: {3}
'''
    update_time = '2019.05.23'
    script_number = script_num()
    author = 'LRX'
    version = 'v1.0'

    ConsoleLogger.Info(logo.format(author,version,update_time,script_number))

def script_num():
    count = 0
    for (root, dirs, files) in os.walk(paths.script):
        for f in files:
            if f.split('.')[1] == 'py' and f.split('.')[0] != '__init__':
                count += 1
    return count
