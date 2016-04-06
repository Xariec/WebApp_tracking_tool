import pymongo
import re


the_file = "test.txt"
user = "Xariec"

dev = True

if dev == True:
	db = pymongo.Connection('localhost', 27017).dev
else:
	db = pymongo.Connection('localhost', 27017).cc

def bR(the_file, user):
	count = 0
	dup = 0
	with open(the_file) as f:
		defend = False
		status = "Victory"
		p1 = user
		for line in f:
			if re.search(r"Player:", line):
				p1 = line[8:].rstrip()
			elif re.search(r"2015", line):
				date = line.rstrip()
			elif re.search( r" at", line):
				if line[:8] == "Defended":
					defend = True
				elif line[:8] == "Attacked":
					defend = False
				p2 = line[9:line.find(" at")]
				sector = line[line.find(" at")+3:].rstrip()
				sector = sector.split(",")
				x = int(sector[0])
				y = int(sector[1])
			elif re.search(r"DEFEAT", line):
				if defend == True:
					status = "Victory"
				elif defend == False:
					status = "Defeat"
			elif re.search(r"VICTORY", line):
				if defend == False:
					status = "Victory"
				elif defend == True:
					status = "Defeat"
			if re.search(r"Expand", line):
				duplicateCheck = db.brs.find_one({'time' : date, 'x' : x, 'y' : y})
				if duplicateCheck:
					dup += 1
				else:
					if defend == False:
						attacker = p1
						defender = p2						
					else:
						attacker = p2
						defender = p1
					print x,y,attacker, defender, status
					query = db.sector_map.find_one({'x' : x, 'y' : y})
					if query['last_update'] < date or query['status'] == "Player":
						
						if defend == False and status == "Victory" or defend == True and status == "Victory":# If the attacker won the battle
							if query['pname'] != attacker and query['last_scan'] < date: # sector not in their name yet
								print " updating sector to attackers name"
								# db.sector_map.update({'x' : x, 'y' : y}, {"$set" : {'pname' : attacker, 'last_scan' : "", 'last_update' : date, 'units' : [], 'defense' : "", 'products' : [], 'alliance' : "", 'status' : "Player"}})
								# db.sector_map.update({'x' : x, 'y' : y},{"$push": {'updates' : {'player' : attacker, 'source' : "Battle Report", 'status' : "Player", 'time' : date, 'user' : user }}})
							elif query['pname'] == attacker: # The sector was already in their name
								print " sector already belongs to attacker"
								# db.sector_map.update({'x' : x, 'y' : y},{"$push": {'updates' : {'player' : attacker, 'source' : "Battle Report", 'status' : "Player", 'time' : date, 'user' : user }}})
						elif defend == True and status == "Defeat" or defend == False and status == "Defeat": # Attacker lost the battle
							print " Attacker Lost, no sector update"
							# db.sector_map.update({'x' : x, 'y' : y},{"$push": {'updates' : {'player' : defender, 'source' : "Battle Report", 'status' : "Player", 'time' : date, 'user' : user }}})
							if query['pname'] != defender: #Update sector to defenders name
								print " Didn't know defender Owned sector"
								# db.sector_map.update({'x' : x, 'y' : y}, {"$set" : {'pname' : defender, 'last_scan' : "", 'last_update' : date, 'units' : [], 'defense' : "", 'products' : [], 'alliance' : "", 'status' : "Player"}})
								
					else:
						print ""
						# db.sector_map.update({'x' : x, 'y' : y},{"$push": {'updates' : {'player' : attacker, 'source' : "Battle Report", 'status' : "Player", 'time' : date, 'user' : user }}})
					# db.sector_map.update({'x' : x, 'y' : y},{"$push": { 'battles' : {'attacker' : attacker, 'defender' : defender, 'outcome' : status, 'time' : date, 'user' : user }}})
					# db.brs.insert({'x' : x, 'y' : y, 'attacker' : attacker, 'defender' : defender, 'outcome' : status, 'time' : date, 'user' : user})
					# print "%d,%d, attacker : %s, defender : %s" %(x,y,attacker,defender)
					print ""
					
			count += 1

bR(the_file, user)				