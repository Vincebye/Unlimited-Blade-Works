import requests
from lib.core.data import headers,realman
from lib.utils.cmsdata import cms_dict
from lib.core.enums import LOGGING_MESSAGE
from lib.core.log import ConsoleLogger
from lib.core.data import conf,realman
# def fingerprint():
#     pass

# def header_probe(target_url):
#     try:
#         header=requests.get(target_url,headers=headers).headers
#         print(type(header))
#     except Exception as e:
#         print(e)
#     realman.timo=header
    #realman.timo.extend(header)
headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
import re
import hashlib

realman.timo.cms='Unknow'

def getMD5(password):
    m = hashlib.md5()
    m.update(password.encode('utf-8'))
    return m.hexdigest()

def makeurl(url):
    prox = "http://"
    if(url.startswith("https://")):
        prox = "https://"
    url_info = urlparse.urlparse(url)
    url = prox + url_info.netloc + "/"

    return url

def isMatching(f_path, cms_name, sign, res, code, host, head):
    ConsoleLogger.Info(LOGGING_MESSAGE.CMS_SCAN_RUNNING.format(cms=cms_name))

    isMatch = False
    if f_path.endswith(".gif"):
        if sign:
            isMatch = getMD5(res) == sign
        else:
            isMatch = res.startswith("GIF89a")

    elif f_path.endswith(".png"):
        if sign:
            isMatch = getMD5(res) == sign
        else:
            isMatch = res.startswith("\x89PNG\x0d\x0a\x1a\x0a")

    elif f_path.endswith(".jpg"):
        if sign:
            isMatch = getMD5(res) == sign
        else:
            isMatch = res.startswith("\xff\xd8\xff\xe0\x00\x10JFIF")

    elif f_path.endswith(".ico"):
        if sign:
            isMatch = getMD5(res) == sign
        else:
            isMatch = res.startswith("\x00\x00\x00")

    elif code == 200:
        if sign and res.find(sign) != -1 or str(head).find(sign) != -1:
            isMatch = True

    elif sign and str(head).find(sign) != -1:
        isMatch = True

    if isMatch:
        ConsoleLogger.Info(LOGGING_MESSAGE.CMS_SCAN_FOUND.format(url=host,cms=cms_name))
        realman.timo.cms=cms_name
        return True

    return False

def assign(service, arg):
    if service == "www":
        return True,makeurl(arg)

def audit(arg,realman):
    cms_cache = {}
    cache = {}

    def _cache(url):
        if url in cache:
            return cache[url]
        else:
            try:
                req=requests.get(url,headers=headers,verify=False,timeout=3)
                status_code=req.status_code
                header=req.headers
                html_body=req.text

                if status_code != 200 or not html_body:
                    html_body = ""

                cache[url] = (status_code, header, html_body)
                return status_code, header, html_body
            except Exception as e:
                pass

    for cmsname in cms_dict:
        cms_hash_list = cms_dict[cmsname]

        for cms_hash in cms_hash_list:
            if isinstance(cms_hash, tuple):
                f_path, sign = cms_hash
            else:
                f_path, sign = cms_hash, None

            if not isinstance(f_path, list):
                f_path = [f_path]

            for file_path in f_path:
                if file_path not in cms_cache:
                    cms_cache[file_path] = []
                cms_cache[file_path].append((cmsname, sign))

    cms_key = cms_cache.keys()
    #cms_key.sort(key=len)

    isMatch = False

    for f_path in cms_key:
        if isMatch:
            break
        for cms_name, sign in cms_cache[f_path]:
            code, head, res = _cache(arg + f_path)
            isMatch =isMatching(f_path, cms_name, sign, res, code, arg, head)
            if isMatch:
                break

def whatcms():
    if conf.url:
        ConsoleLogger.Info(LOGGING_MESSAGE.CMS_SCAN_START.format(url=conf.url))
        audit(conf.url,realman)

