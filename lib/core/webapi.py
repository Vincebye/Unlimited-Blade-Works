import importlib
import sys
import os
from lib.core.log import ConsoleLogger
import pymongo
from datetime import datetime

#scriptPath='/Users/liuzhihong/Dropbox/Unlimited-Blade-Works/script'
scriptPath=os.getcwd()+'/script'
sys.path.append(scriptPath)



class UBW_Scan(object):
    def __init__(self,target,pocname):
        self.target=target
        self.poc_name=pocname
        self.poc_obj=importlib.import_module(pocname,package='script')
        self.conn = pymongo.MongoClient('127.0.0.1', 27017, socketTimeoutMS=3000)

    def scan(self):
        if isinstance(self.target,str):
            result=self.poc_obj.poc(self.target)
            self.save2mongo(self.conn,self.target,self.poc_name,result)
        if isinstance(self.target,list):
            result=[]
            for i in self.target:
                result.append(i+self.poc_obj.poc(i))
            for i in result:
                self.save2mongo(self.conn,self.target,self.poc_name,i)
    
    def save2mongo(self,conn,target,pocname,result,create_time=datetime.now()):
        db = conn.test
        collection = db.scan_result
        scan_task = {
            'url': target,
            'pocname': pocname,
            'result': result,
            'create_time':create_time
        }
        result = collection.insert(scan_task)

# a=UBW_Scan('127.0.0.1','test')
#print(a.poc_obj)
