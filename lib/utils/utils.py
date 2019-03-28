import socket
def url2ip(url):
    try:
        ip=socket.gethostbyname(url)
        return ip
    except Exception as e:
        print(e)
