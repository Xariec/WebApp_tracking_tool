import pymongo
import sys
import re
import bson
from bson.objectid import ObjectId

db = pymongo.Connection('localhost', 27017).cc




def parse(filename, user):
	insert_count = 0
	duplicate_count = 0
	lines = open(filename, "r").readlines()
	for x in lines:
		if re.search(r"2014", x ) or re.search(r"2015", x):
			date = x.strip()
		elif re.search(r"Inbound warp detected", x):
			destination = x.find("!")
			source = x.find(".")
			dest = x[25:destination].split(",")
			origin = x[destination+27:source].split(",")
			x_origin = int(origin[0])
			y_origin = int(origin[1])
			x_dest = int(dest[0])
			y_dest = int(dest[1])
			duplicateCheck = db.warps.find_one({'time' : date, 'x_origin' : x_origin, 'y_origin' : y_origin})
			if duplicateCheck:
				duplicate_count +=1
			else:
				dest = db.sector_map.find_one({'x' : x_dest, 'y' : y_dest})
				origin = db.sector_map.find_one({'x' : x_origin, 'y' : y_origin})
				pname = origin['pname']
				db.warps.insert({'time' : date, 'x_origin' : x_origin, 'y_origin' : y_origin, 'x_dest': x_dest, 'y_dest' : y_dest, 'player' : pname})
				db.sector_map.update({'x' : x_origin, 'y' : y_origin},{"$push": { 'outgoing_warps' : {'time' : date, 'x_dest': x_dest, 'y_dest' : y_dest, 'player' : pname}}})
				if dest['status'] != "Player" or dest['status'] == "Player" and dest['pname'] != pname and dest['last_update'] < date or dest['status'] == "Player" and dest['pname'] == "":
					db.sector_map.update({'x' : x_dest, 'y' : y_dest}, {"$set" : {'status' : "Player", 'pname' : pname, 'last_update' : date, 'last_scan' : "", 'defense' : "", 'units' : [], 'products' : []}})
					db.sector_map.update({'x' : x_dest, 'y' : y_dest},{"$push": { 'incoming_warps' : {'time' : date, 'x_origin': x_origin, 'y_origin' : y_origin, 'player' : pname}, 'updates' : {'player' : pname, 'source' : "warp", 'status' : "Player", 'time' : date, 'user' : user }}})
				else:
					db.sector_map.update({'x' : x_dest, 'y' : y_dest}, {"$push": { 'incoming_warps' : {'time' : date, 'x_origin': x_origin, 'y_origin' : y_origin, 'player' : pname}, 'updates' : {'player' : pname, 'source' : "warp", 'status' : "Player", 'time' : date, 'user' : user }}})
				insert_count +=1
	return (insert_count, duplicate_count)





if __name__ == '__main__':
	print parse("inbound.txt", "Xariec")
	






