import re
import time
import datetime
import pymongo

db = pymongo.Connection('localhost', 27017).cc

def sectorLog(the_file):
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')	
	with open(the_file) as f:
		db.sectorKeeper.insert({'time' : st, 'leaderboard' : []})
		
		for line in f:
			if re.search(r"\d", line):
				if "(" not in line:
					rank = int(line[0:3].split("\t")[0])
					sector =  int(line[2:].lstrip("\t").split("\t")[0].replace(",",""))
					name = line[2:].lstrip("\t").split("\t")[1].replace("*","").rstrip("\n\r")
					name = name.rstrip(" VM")
					if rank < 100:
						db.sectorKeeper.update({'time' : st}, {"$push" : {'leaderboard' : {'rank' : rank, 'sector' : sector, 'name' : name}}})
						query_hw = db.homeworlds.find_one({'pname' : name})
						if query_hw:
							db.homeworlds.update({'_id' : query_hw['_id']}, {"$push" : {'sector_count' : {'sector' : sector, 'time' : st}}})
						else:
							db.homeworlds.insert({'pname' : name, 'x' : 0, 'y' : 0, 'time' : st, 'type' : "", 'updates' : [], 'alias' : [], 'relation' : ""})
							db.homeworlds.update({'pname' : name}, {"$push" : {'sector_count' : {'rank' : rank, 'sector' : sector, 'time' : st}}})
							
		uploaded = db.sectorKeeper.find_one({'time' : st})			
	return(uploaded)

					
					
