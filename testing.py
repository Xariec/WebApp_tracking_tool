import pymongo
db = pymongo.Connection('localhost', 27017).cc


date = "03-02"
print date
query = db.sector_map.find({'status' : "Player", 'last_scan' :  "", 'last_update' : {"$regex" : date}}).sort('last_update', 1).limit(1)
# query = db.sector_map.find({'status' : "Player", 'last_scan' : "", 'last_update' : {"$regex" : "/03-02/"}})

gt = ""

for a in query:
	gt += a['last_update']
	
query2 = db.sector_map.find({'status' : "Player", 'last_scan' :  "", 'last_update' : {"$gt" : gt}})

for a in query2:
	print a['last_update']