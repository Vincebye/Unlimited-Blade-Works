import os
import requests
from lib.core.data import headers
from lib.utils.debug import debug_print
import time
test=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
def poc(target):
    try:
        code=requests.get(target,headers=headers).status_code
        if code==200:
            return True
    except Exception as e:
        print(e)
        
