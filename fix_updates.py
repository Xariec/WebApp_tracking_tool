import re
import pymongo


db = pymongo.Connection('localhost', 27017).cc


badHW = db.homeworlds.find({'x' : 0, 'y' : 0})

for a in badHW:
	print a['pname']






# values = ["status", "player", "time", "user", "source"]


# query = db.sector_map.find()

# for a in query:
	# updates = a['updates']
	# for b in updates:
		# if "inserted" in b:
			# status_start = b[:25].find("'")+1
			# status_end = b[status_start:status_start+20].find("'")
			# status =  b[status_start:status_start + status_end].rstrip(" ")
			# time = '2014-12-10 16:32:48'
			# source = "insert"
			# user = "Xariec"
			# player = ""
			
			


# for a in updates:
	# if "Sector inserted" in a:
		# # I think i'm just going to delete the original updates
		# b = a.find("'")
		# status = a[b+1:b+7]
		# c = a.find("during '")
		# print "Initial Insert"
	# elif "Sector became" in a:
		# if "map" in a:
			# # print "Sector update from map"
			# # print a
			# status_start = a.find("'")+1
			# status_end = status_start + a[status_start:].find("'")
			# status = a[status_start:status_end]
			# source = "manual"
			# user = "Xariec"
			# time_start = a.find("'201")+1
			# time_end = a[time_start:].find("'")+time_start
			# time = a[time_start:time_end]
			# print "Status : %s, player : %s, User : %s, Time: %s" %(status,player,user,time)
			# print status
			
	# elif "gained control" in a:
		# print "Scan update"
	# elif "Sector update" in a:
		# print "Warp Update"
