## -*- coding: utf-8 -*-
import re
import web
import hashlib
import pymongo
from bson.objectid import ObjectId
import time
import datetime


db = pymongo.Connection('localhost', 27017).cc



class MongoStuff(object):

	def playerUpdate(self, post):
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		x = int(post['x'])
		y = int(post['y'])
		alliance = post['alliance']
		relation = post['relation']
		pname = post['pname']
		query = db.homeworlds.find_one({'x' : x, 'y' : y})
		if query:
			if pname == query['pname'] or pname == "":
				db.homeworlds.update({'x' : x, 'y' : y}, {"$set" : {'alliance' : alliance, 'relation' : relation}})
			else:
				# db.sector_map.update({'pname' : query['pname']},{"$set" : {'pname' : pname}}, multi=True)
				ow = db.sector_map.find({'outgoing_warps' : {"$elemMatch" : {'player' : query['pname']}}})
				for a in ow:
					db.sector_map.update({'outgoing_warps' : {"$elemMatch" : {'player' : query['pname']}}}, {"$set" : {'outgoing_warps.player' : pname}}) 
				# db.sector_map.update({'outgoing_warps.player' : query['pname']},{"$set" : { 'outgoing_warps.$.player' : pname}}, multi=True)
				# db.sector_map.update({'incoming_warps.player' : query['pname']},{"$set" : { 'incoming_warps.$.player' : pname}}, multi=True)
				# db.sector_map.update({'updates.player' : query['pname']},{"$set" : { 'updates.$.player' : pname}}, multi=True)
				# db.sector_map.update({'battles.attacker' : query['pname']},{"$set" : { 'battles.$.attacker' : pname}}, multi=True)
				# db.sector_map.update({'battles.defender' : query['pname']},{"$set" : { 'battles.$.defender' : pname}}, multi=True)
				# db.sectorKeeper.update({'leaderboard.name' : query['pname']},{"$set" : { 'leaderboard.$.name' : pname}}, multi=True)
				# db.scoreKeeper.update({'leaderboard.name' : query['pname']},{"$set" : { 'leaderboard.$.name' : pname}}, multi=True)
				# db.warps.update({'player' : query['pname']}, {"$set" : {'player' : pname}}, multi=True)
				
				# db.homeworlds.update({'_id' : query['_id']}, {"$set" : {'pname' : pname, 'alliance' : alliance, 'relation' : relation}})
				# db.homeworlds.update({'_id' : query['_id']}, {"$push" : {'alias' : {'Player' : query['pname'], 'time' : st}}})



	def returnAlliance(self, alliance):
		plist = []
		players = db.homeworlds.find({'alliance' : alliance})
		for a in players:
			plist.append(str(a['pname']))
		print plist
		sectors = db.sector_map.find({'pname' : {"$in" : plist}})
		return sectors
			
			

	
	def userUpdates(self, user, time, action, info):
		db.users.update({'username' : user},{"$push" :{'updates' : {'time' : time, 'action' : action, 'info' : info}}})

	def homeworldList(self):
		self.hw = []
		self.query = db.homeworlds.find().sort('pname' ,1)
		for a in self.query:
			if a['pname'] not in self.hw:
				self.hw.append((a['pname']))
				
		return self.hw
	
	def scoreTime(self):
		self.times = []
		self.query = db.scoreKeeper.find().sort('time', -1)
		for a in self.query:
			self.times.append((a['time']))
		
		return self.times
		
	def sectorTime(self):
		self.times = []
		self.query = db.sectorKeeper.find().sort('time', -1)
		for a in self.query:
			self.times.append((a['time']))
		
		return self.times
		
	def mapTime(self):
		self.map = db.map_time.find().sort('utime', -1)
		self.map_times = []
		for a in self.map:
			self.map_times.append((a['utime']))
			
		return self.map_times
		
	def listPlayerSectors(self, time1, time2):
		self.players = []
		self.first.append((db.map_snapshots.find_one({'utime' : time1})['map']))
		self.second.append((db.map_snapshots.find_one({'utime' : time2})['map']))
		for i in range(len(self.first[0])):
			if self.first[0][i][2] !=self.second[0][i][2]:
				if self.second[0][i][2] == "Player":
					# print self.second[0][i][2]
					self.count_player +=1
					self.player.append((db.sector_map.find({'x' : self.second[0][i][0], 'y' : self.second[0][i][1]})))
		return (self.player)
		
	def returnMap(self, time1, time2):
		self.sectors = []
		self.first = []
		self.second = []
		self.count = 0
		self.first.append((db.map_snapshots.find_one({'utime' : time1})['map']))
		self.second.append((db.map_snapshots.find_one({'utime' : time2})['map']))
		for i in range(len(self.first[0])):
			if self.first[0][i][2] !=self.second[0][i][2]:
				# print self.second[0][i][2]
				self.count +=1
				self.query = db.sector_map.find({'x' : self.second[0][i][0], 'y' : self.second[0][i][1]})
				for a in self.query:
					if a['status'] == "Player":
						self.sectors.append((a))
				# elif self.second[0][i][2] == "Rebel":
					# self.player.append((db.sector_map.find_one({'x' : self.second[0][i][0], 'y' : self.second[0][i][1]})))	
		return (self.sectors)
		

			
	def sectorList(self):
		self.sector_list = []
		self.query = db.sector_map.find({'status' : "Player"}).sort([('pname', 1),('x', 1),('y', 1)]).limit(1000)
		for a in self.query:
			self.sector_list.append((a))
		return self.sector_list
		
		
	def sectorListPlayer(self,pname):
		self.sector_list = []
		self.query = db.sector_map.find({'pname' : pname}).sort([('x', -1),('y', -1)]).limit(5000)
		for a in self.query:
			self.sector_list.append((a))
		return self.sector_list		

		
	
	def playerList(self, access):
		self.list = []
		self.query = db.homeworlds.find().sort('pname', 1)
		if access < 3:
			for a in self.query:
				if a['pname'] != "" and a['pname'] not in self.list and a['current_sectors'] > 1:
					if a['relation'] != "Friendly":
						self.list.append((a['pname']))
		elif access >= 3:
			for a in self.query:
				if a['pname'] != "" and a['pname'] not in self.list and a['current_sectors']  > 1:
					self.list.append((a['pname']))

		return self.list
		
	def alliances(self, access):
		self.list = []
		self.query = db.alliance.find({})
		if access == 1:
			self.list.append(("Collection"))
			self.list.append(("The Boys Are Back!"))
		
		elif access == 2:
			for a in self.query:
				if a['ALLIANCE_NAME'] != "United We Stand":
					self.list.append((str(a['ALLIANCE_NAME'])))
		elif access >= 3:
			for a in self.query:
				self.list.append((str(a['ALLIANCE_NAME'])))
		return self.list
		
		
	def sectorSizes(self):
		self.list = []
		self.query = db.sector_map.find({'size' : {"$ne" : ""}}).sort('size', -1)
		for a in self.query:
			if a['size'] not in self.list:
				self.list.append((str(a['size'])))
		return self.list

	def findRange(self, x,y):
		self.x = int(x)
		self.xmin = self.x - 5
		self.xmax = self.x + 5
		self.y = int(y)
		self.ymin = self.y - 5
		self.ymax = self.y + 5
		self.range = db.sector_map.find({'x' : {"$gte" : self.xmin, "$lte" : self.xmax}, 'y' : {"$gte" : self.ymin, "$lte" : self.ymax}})
		return self.range

	def findSector(self, x,y):
		self.x = int(x)
		self.y = int(y)
		self.sector = db.sector_map.find_one({'x' : self.x, 'y' : self.y})
		return self.sector
	
	def comparePlayers(self, p1,p2):
		self.p1_sectors = []
		self.p2_sectors = []
		self.p1_query = db.sector_map.find({'status' : "Player", 'pname' : p1})
		self.p2_query = db.sector_map.find({'status' : "Player", 'pname' : p2})
		for a in self.p1:
			self.p1_sectors.append((a))
		for b in self.p2:
			self.p2_sectors.append((b))
			

		
		
		
	def updateSector(self, post, user):
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		x = int(post['x'])
		y = int(post['y'])
		if post['status'] != "Player":
			db.sector_map.update({'x' : x, 'y': y }, {"$set" : {'last_update' : st, 'size' : post['size'], 'status' : post['status'],'asp' : "NO", 'sdi' : "NO", 'pname' : "", 'corporate_factory' : "NO",  'wada' : "NO", 'defense' : "", 'last_scan' : "", 'units' : [], 'alliance' : "" }})
			db.sector_map.update({'x' : x, 'y' : y},{"$push": { 'updates' : {'player' : "", 'source' : "manual", 'status' : post['status'], 'time' : st, 'user' : user }}})

		else:
			query = db.sector_map.find_one({'x' : x, 'y': y })
			if post['player'] == query['pname'] or post['player'] == "":
				db.sector_map.update({'x' : x, 'y': y }, {"$set" : {'last_update' : st, 'asp' : post['asp'], 'sdi' : post['sdi'], 'type' : post['type'], 'corporate_factory' : post['CF'], 'wada' : post['wada'], 'size' : post['size']}})
				db.sector_map.update({'x' : x, 'y' : y},{"$push": { 'updates' : {'player' : query['pname'], 'source' : "manual", 'status' : post['status'], 'time' : st, 'user' : user }}})
			elif  post['player'] != query['pname'] and post['player'] != "":
				db.sector_map.update({'x' : x, 'y': y }, {"$set" : {'pname' : post['player'], 'last_update' : st, 'asp' : post['asp'], 'sdi' : post['sdi'], 'type' : post['type'], 'corporate_factory' : post['CF'], 'wada' : post['wada'], 'size' : post['size'], 'units' : []}})
				db.sector_map.update({'x' : x, 'y' : y},{"$push": { 'updates' : {'player' : post['player'], 'source' : "manual", 'status' : post['status'], 'time' : st, 'user' : user }}})
				if post['type'] == "HomeWorld" or post['type'] == "HomeWorld/WarpGate":
					query = db.homeworlds.find_one({'x' : x, 'y' : y})
					if query:
						if query['pname'] != post['player']:
							db.homeworlds.update({'_id' : query['_id']}, {"$set" : {'pname' : post['player']}})
							db.homeworlds.update({'_id' : query['_id']}, {"$push" : {'alias' : query['pname']}})
					else:
						db.homeworlds.insert({'pname' : post['player'], 'x' : x, 'y' : y, 'time' : st, 'type' : post['type'], 'updates' : [], 'alias' : []})

		
	def userControl(self):
		self.query = db.users.find()
		self.users = []
		for a in self.query:
			self.users.append((a))
		return self.users
		
	def updateAccess(self, u_id, access):
		db.users.update({'_id' : ObjectId(u_id)}, {"$set" : {'access' : access}})
		
	def sectorLog(self, the_file):
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
								db.homeworlds.update({'_id' : query_hw['_id']}, {"$set" : {'current_sectors' : sector}})
							else:
								db.homeworld_tmp.insert({'pname' : name, 'x' : 0, 'y' : 0, 'time' : st, 'type' : "", 'updates' : [], 'alias' : [], 'relation' : ""})
								db.homeworld_tmp.update({'pname' : name}, {"$push" : {'sector_count' : {'rank' : rank, 'sector' : sector, 'time' : st}}})
								
			uploaded = db.sectorKeeper.find_one({'time' : st})
		return(uploaded)
	
	
	def scoreLog(self, the_file):
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')	
		with open(the_file) as f:
			db.scoreKeeper.insert({'time' : st, 'leaderboard' : []})
			
			for line in f:
				if re.search(r"\d", line):
					if "(" not in line:
						rank = int(line[0:3].split("\t")[0])
						name = line[4:].lstrip("\t").split("\t")[1].replace("*","").rstrip("\n\r")
						score =  int(line[2:].lstrip("\t").split("\t")[0].replace(",",""))
						name = name.rstrip(" VM")
						if rank < 100:
							db.scoreKeeper.update({'time' : st}, {"$push" : {'leaderboard' : {'rank' : rank, 'score' : score, 'name' : name}}})
							query_hw = db.homeworlds.find_one({'pname' : name})
							if query_hw:
								db.homeworlds.update({'_id' : query_hw['_id']}, {"$push" : {'score' : {'score' : score, 'time' : st}}})
								db.homeworlds.update({'_id' : query_hw['_id']}, {"$set" : {'current_score' : score}})
							else:
								db.homeworld_tmp.insert({'pname' : name, 'x' : 0, 'y' : 0, 'time' : st, 'type' : "", 'updates' : [], 'alias' : [], 'relation' : ""})
								db.homeworlds_tmp.update({'pname' : name}, {"$push" : {'score' : {'rank' : rank, 'score' : score, 'time' : st}}})
								
			uploaded = db.scoreKeeper.find_one({'time' : st})			
		return(uploaded)
		
	def bR(self, the_file, user):
		count = 0
		dup = 0
		with open(the_file) as f:
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
						hw = db.homeworlds.find_one({'x' : x, 'y' : y})
						if hw:
							print "HW Found"
							db.sector_map.update({'x' : x, 'y' : y},{"$push": { 'battles' : {'attacker' : attacker, 'defender' : defender, 'outcome' : status, 'time' : date, 'user' : user }}})
							db.brs.insert({'x' : x, 'y' : y, 'attacker' : attacker, 'defender' : defender, 'outcome' : status, 'time' : date, 'user' : user})
							count +=1
						else:
							
							query = db.sector_map.find_one({'x' : x, 'y' : y})
							if query['last_update'] < date or query['status'] == "Player":
								db.sector_map.update({'x' : x, 'y' : y},{"$push": { 'battles' : {'attacker' : attacker, 'defender' : defender, 'outcome' : status, 'time' : date, 'user' : user }}})
								print "Last update older or sector is player"
								if defend == False and status == "Victory" or defend == True and status == "Victory":# If the attacker won the battle
									if query['pname'] != attacker and query['last_scan'] < date: # sector not in their name yet
										print " updating sector to attackers name"
										db.sector_map.update({'x' : x, 'y' : y}, {"$set" : {'pname' : attacker, 'last_scan' : "", 'last_update' : date, 'units' : [], 'defense' : "", 'products' : [], 'alliance' : "", 'status' : "Player"}})
										db.sector_map.update({'x' : x, 'y' : y},{"$push": {'updates' : {'player' : attacker, 'source' : "Battle Report", 'status' : "Player", 'time' : date, 'user' : user }}})
									elif query['pname'] == attacker: # The sector was already in their name
										print " sector already belongs to attacker"
										db.sector_map.update({'x' : x, 'y' : y},{"$push": {'updates' : {'player' : attacker, 'source' : "Battle Report", 'status' : "Player", 'time' : date, 'user' : user }}})
								elif defend == True and status == "Defeat" or defend == False and status == "Defeat": # Attacker lost the battle
									print " Attacker Lost, no sector update"
									db.sector_map.update({'x' : x, 'y' : y},{"$push": {'updates' : {'player' : defender, 'source' : "Battle Report", 'status' : "Player", 'time' : date, 'user' : user }}})
									if query['pname'] != defender: #Update sector to defenders name
										print " Didn't know defender Owned sector"
										db.sector_map.update({'x' : x, 'y' : y}, {"$set" : {'pname' : defender, 'last_scan' : "", 'last_update' : date, 'units' : [], 'defense' : "", 'products' : [], 'alliance' : "", 'status' : "Player"}})
										
							else:
								print ""
								db.sector_map.update({'x' : x, 'y' : y},{"$push": {'updates' : {'player' : attacker, 'source' : "Battle Report", 'status' : "Player", 'time' : date, 'user' : user }}})
								db.sector_map.update({'x' : x, 'y' : y},{"$push": { 'battles' : {'attacker' : attacker, 'defender' : defender, 'outcome' : status, 'time' : date, 'user' : user }}})
							db.brs.insert({'x' : x, 'y' : y, 'attacker' : attacker, 'defender' : defender, 'outcome' : status, 'time' : date, 'user' : user})
							print ""
							
							count += 1
										
					
		return(count, dup)
