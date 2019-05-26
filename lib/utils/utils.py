import socket
from urllib.parse import urlparse,urljoin
def url2ip(url):
    '''
    @description: url转ip
    @url {str} :待转换URL
    @return: 
    '''
    try:
        url=url if url.startswith('http') else 'http://'+url
        url=urlparse(url).netloc
        ans = [i for i in socket.getaddrinfo(url.split(':')[0], None)[0][4] if i != 0][0]
        if ':' in url:
            ans += ':' + url.split(':')[1]
        return ans
    except Exception as e:
        return url

def check_tcp_port(ip,port,timeout=3):
    '''
    @description: 检查端口是否开启
    @ip {str} 检测IP
    @port {int} 检测port
    @return: 
    '''
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(timeout)
    try:
        sk.connect((target, port))
        return True
    except Exception:
        return False