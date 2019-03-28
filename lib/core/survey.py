import requests
from lib.core.data import headers,realman
def fingerprint():
    pass

def header_probe(target_url):
    try:
        header=requests.get(target_url,headers=headers).headers
        print(type(header))
    except Exception as e:
        print(e)
    realman.timo=header
    #realman.timo.extend(header)
