import socket

result=[]
def poc(target):
    try:
        ip=socket.gethostbyname(target)
        result.append(ip)
    except: 
        pass
    print(result)