from lib.core.data import cfg
from lib.utils.debug import compare
import requests
import json
import re
class ZoomEye():
    def __init__(self):
        self.username=cfg.get('zoomeye','zoomeye_username')
        self.password=cfg.get('zoomeye','zoomeye_password')

    def get_access(self):
        data={"username":self.username,"password":self.password}
        test=requests.post('https://api.zoomeye.org/user/login',data=json.dumps(data))
        return test.text

    def query(self,keyword,num=20):
        access_key=self.get_access().split('"')[3]
        match_result=[]
        page=num//20
        rule=re.compile(r'\"ip\": \"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\"')
        headers={"Authorization": 'JWT '+ access_key}
        for i in range(page):
            url='https://api.zoomeye.org/host/search?query={keyword}&page={page}'.format(keyword=keyword,page=(i+1))
            text=requests.get(url,headers=headers).text
            result=rule.findall(text)
            match_result.extend(result)
        return match_result
    
    