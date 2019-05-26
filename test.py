import pymongo
conn = pymongo.MongoClient('127.0.0.1', 27017, socketTimeoutMS=3000)
db=conn.test
result=db.scan_result.find({})
for i in result:
	print(i['url'])