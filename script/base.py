from datetime import datetime

class BasePoc(object):
    def __init__(self,name,auther='LRX',product='Unknown',vultype='Unauth',create_time=datetime.now,eg_target='127.0.0.1'):
        self.name=name
        self.auther=auther
        self.product=product
        self.vultype=vultype
        self.create_time=create_time
        self.eg_target=eg_target

    def poc(self,target):
        pass

