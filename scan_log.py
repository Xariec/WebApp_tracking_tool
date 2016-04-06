#!c:/python27/python.exe

import re
import time
import datetime
import pymongo
db = pymongo.Connection('localhost', 27017).cc

def scanLog(the_file, user):
	debug = 0
	with open(the_file) as f:
		user = user
		inserted = 0
		skipped = 0
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

		alliance = ""
		reactor = ""
		reactor_lvl = ""
		reactor_qty = 0
		tcc = ""
		tcc_lvl = ""
		corporate_factory = "NO"
		tcc_qty = 0
		star_ship = ""
		star_ship_lvl = ""
		star_ship_qty = 0
		ore = ""
		ore_lvl = ""
		ore_qty = 0
		crystal = ""
		crystal_lvl = ""
		crystal_qty = 0
		research = ""
		research_lvl = ""
		research_qty = 0
		population = ""
		population_lvl = ""
		population_qty = 0
		warp_gate = ""
		warp_gate_lvl = ""
		warp_gate_qty = 0
		defense = ""
		defense_lvl = ""
		defense_qty = 0
		sdi = "NO"
		asp = "NO"
		wada = "NO"
		dmg = 0
		dagger = 0
		dagger_mv = 0
		hydra = 0
		hydra_mv = 0
		jackal = 0
		jackal_mv = 0
		morningstar = 0
		morningstar_mv = 0
		firefly = 0
		firefly_mv = 0
		wyvern = 0
		wyvern_mv = 0
		paladin = 0
		paladin_mv = 0
		warlock = 0
		warlock_mv = 0
		warlock_st = 0
		scarab = 0
		aesir = 0
		aesir_mv = 0
		broadsword = 0
		broadsword_mv = 0
		sf_m44 = 0
		tc_0106 = 0
		tc_1212 = 0
		tc_912 = 0
		online = ""
		dg1 = 0
		dg2 = 0
		dg3 = 0
		dg4 = 0
		dg5 = 0
		
		
		
		for line in f:
			# SECTOR BASE INTEL
			if re.search(r"2014", line ) or re.search(r"2015", line):
				date = line.strip()
			elif re.search( r"SECTOR:", line):
				sector = line[7:].strip()
			elif re.search( r"CONTROLLED BY:", line):
				pname = line[14:].strip()
			elif re.search( r"ALLIANCE:", line):
				alliance = line[9:].strip()
			elif re.search( r"SIZE:", line):
				size = line[5:].strip()
			elif re.search( r"HOMEWORLD:", line):
				homeworld = line[10:].strip()
			elif re.search( r"ONLINE:", line):
				online = line[8:].strip()
			
			# BUILDING DATA		
			elif re.search( r"SINGULARITY REACTOR", line):
				reactor = line[23:].split(':')
				reactor_lvl = reactor[0]
				reactor_qty = int(reactor[1].strip('\t,\n'))
			elif re.search( r"STARSHIP FOUNDRY", line):
				star_ship = line[20:].split(':')
				star_ship_lvl = star_ship[0]
				star_ship_qty = int(star_ship[1].strip('\t,\n'))
			elif re.search( r"TACTICAL", line):
				tcc = line[27:].split(':')
				tcc_lvl = tcc[0]
				tcc_qty = int(tcc[1].strip('\t,\n'))
			elif re.search( r"KINETIC MATERIALIZER", line):
				ore = line[24:].split(':')
				ore_lvl = ore[0]
				ore_qty = int(ore[1].strip('\t,\n'))
			elif re.search( r"CATALYST INJECTION FIELD", line):
				crystal = line[28:].split(':')
				crystal_lvl = crystal[0]
				crystal_qty = int(crystal[1].strip('\t,\n'))
			elif re.search( r"MASS INCUBATION PLANT", line):
				population = line[25:].split(':')
				population_lvl = population[0]
				population_qty = int(population[1].strip('\t,\n'))
			elif re.search( r"ARCHIVES OF ENLIGHTENMENT", line):
				research = line[29:].split(':')
				research_lvl = research[0]
				research_qty = int(research[1].strip('\t,\n'))
			elif re.search( r"WARP GATE", line):
				warp_gate = line[13:].split(':')
				warp_gate_lvl = warp_gate[0]
				warp_gate_qty = int(warp_gate[1].strip('\t,\n'))
			elif re.search( r"CORPORATE FACTORY", line):
				corporate_factory = "YES"		
			elif re.search( r"SECTOR DEFENSE INTELLIGENCE", line):
				sdi = "YES"
			elif re.search( r"ANOMALY SURVEILLANCE POST", line):
				asp = "YES"
			elif re.search( r"WARP ANOMALY DISPERSION ARRAY", line):
				wada = "YES"
			elif re.search( r"DEFENSE GRID", line):
				defense = line[16:].split(':')
				defense_lvl = defense[0]
				defense_qty = int(defense[1])
				if defense_lvl == "L1":
					dg1 = defense_qty
					dmg += defense_qty*8000
				elif defense_lvl == "L2":
					dg2 = defense_qty
					dmg += defense_qty*16000
				elif defense_lvl == "L3":
					dg3 = defense_qty
					dmg += defense_qty*24000
				elif defense_lvl == "L4":
					dg4 = defense_qty
					dmg += defense_qty*32000
				elif defense_lvl == "L5":
					dg5 = defense_qty
					dmg += defense_qty*40000
					
			elif re.search( r"DAGGER\(", line):
				dagger = int(line[11:].strip().replace(',','').replace(',',''))
				dmg += 1*dagger
			elif re.search( r"DAGGER MV\(", line):
				dagger_mv = int(line[14:].strip().replace(',',''))
				dmg += 2*dagger_mv
			elif re.search( r"FIREFLY\(", line):
				firefly = int(line[12:].strip().replace(',',''))
				dmg += 3*firefly
				dmg += 10*firefly
			elif re.search( r"HYDRA\(", line):
				hydra = int(line[9:].strip().replace(',',''))
				dmg += 1*hydra
			elif re.search( r"JACKAL\(", line):
				jackal = int(line[10:].strip().replace(',',''))
				dmg += 5*jackal
			elif re.search( r"MORNINGSTAR\(", line):
				morningstar = int(line[16:].strip().replace(',',''))
				dmg += 1*morningstar
			elif re.search( r"FIREFLY MV\(", line):
				firefly_mv = int(line[15:].strip().replace(',',''))
				dmg += 2*firefly_mv
				dmg =+ 20*firefly_mv
			elif re.search( r"HYDRA MV\(", line):
				hydra_mv = int(line[13:].strip().replace(',',''))
				dmg += 2*hydra_mv
			elif re.search( r"JACKAL MV\(", line):
				jackal_mv = int(line[14:].strip().replace(',',''))
				dmg += 10*jackal_mv
			elif re.search( r"WYVERN\(", line):
				wyvern = int(line[11:].strip().replace(',',''))
				dmg += 10*wyvern
			elif re.search( r"MORNINGSTAR MV\(", line):
				morningstar_mv = int(line[19:].strip().replace(',',''))
				dmg += 2*morningstar_mv
			elif re.search( r"WYVERN MV\(", line):
				wyvern_mv = int(line[14:].strip().replace(',',''))
				dmg += 20*wyvern_mv
			elif re.search( r"WARLOCK\(", line):
				warlock = int(line[12:].strip().replace(',',''))
				dmg += 1*warlock
			elif re.search( r"PALADIN\(", line):
				paladin = int(line[12:].strip().replace(',',''))
				dmg += 30*paladin
			elif re.search( r"PALADIN MV\(", line):
				paladin_mv = int(line[15:].strip().replace(',',''))
				dmg += 60*paladin_mv
			elif re.search( r"WARLOCK MV\(", line):
				warlock_mv = int(line[15:].strip().replace(',',''))
				dmg += 2*warlock_mv
			elif re.search( r"WARLOCK ST\(", line):
				warlock_st = int(line[15:].strip().replace(',',''))
				dmg += 1*warlock_st
			elif re.search( r"SCARAB\(", line):
				scarab = int(line[11:].strip().replace(',',''))
				dmg += 20*scarab
			elif re.search( r"AESIR\(", line):
				aesir = int(line[10:].strip().replace(',',''))
				dmg += 50*aesir
			elif re.search( r"BROADSWORD\(", line):
				broadsword = int(line[15:].strip().replace(',',''))
				dmg += 10*broadsword
			elif re.search( r"AESIR MV\(", line):
				aesir_mv = int(line[13:].strip().replace(',',''))
				dmg += 100*aesir_mv
			elif re.search( r"BROADSWORD MV\(", line):
				broadsword_mv = int(line[18:].strip().replace(',',''))
				dmg += 20*broadsword_mv
			elif re.search( r"SF-M44", line):
				sf_m44 = int(line[28:].strip().replace(',',''))
			elif re.search( r"TC-0106", line):
				tc_0106 = int(line[30:].strip().replace(',',''))
				dmg += 8000*tc_0106
			elif re.search( r"TC-1212", line):
				tc_1212 = int(line[18:].strip().replace(',',''))
				dmg += 800*tc_1212
			elif re.search( r"TC-912", line):
				tc_912 = int(line[27:].strip().replace(',',''))
				dmg += 1600*tc_912
				
				
				
			elif re.search( r"----- END SEARCH -----", line):
				if debug == 0:
					sector = sector.split(',')
					x = int(sector[0])
					y = int(sector[1])
					
					print "%r,%r" %(x,y)
					print pname, online
					query = db.sector_map.find_one({'x' : x, 'y' : y})
					if date > query['last_scan']:
						if pname == "Rebels" and date > query['last_update']:
							db.sector_map.update({'x' : x, 'y': y }, {"$set" : {'status' : "Rebel", 'size' : size, 'pname' : pname, 'alliance' : alliance, 'type' : "Empty", 'asp' : asp, 'sdi' : sdi, 'wada' : wada, 'defense' : format(dmg, ",d"), 'last_scan' : date, 'last_update' : st}})
							db.sector_map.update({'x' : x, 'y': y }, {"$set" : {'units' : []}})
							db.sector_map.update({'x' : x, 'y' : y},{"$push": { 'updates' : {'player' : pname, 'source' : "scan", 'status' : "Rebel", 'time' : date, 'user' : user }}})
						elif pname == "Centrian Virus" and date > query['last_update']:
							db.sector_map.update({'x' : x, 'y': y }, {"$set" : {'status' : "Centrian", 'size' : size, 'pname' : pname, 'alliance' : alliance, 'type' : "Empty", 'asp' : asp, 'sdi' : sdi, 'wada' : wada, 'defense' : format(dmg, ",d"), 'last_scan' : date, 'last_update' : st}})
							db.sector_map.update({'x' : x, 'y': y }, {"$set" : {'units' : []}})
							db.sector_map.update({'x' : x, 'y' : y},{"$push": { 'updates' : {'player' : pname, 'source' : "scan", 'status' : "Centrian", 'time' : date, 'user' : user }}})
						
						elif pname != "Rebels" or pname !="Centrian Virus":
							if homeworld == "YES" and warp_gate_qty > 0:
								type = "HomeWorld/WarpGate"
								query_hw = db.homeworlds.find_one({'x' : x, 'y' : y})
								if query_hw:
									if query_hw['pname'] != pname:
										db.homeworlds.update({'_id' : query_hw['_id']}, {"$set" : {'pname' : pname, 'last_online' : online}})
										db.homeworlds.update({'_id' : query_hw['_id']}, {"$push" : {'alias' : {'Player' : query_hw['pname'], 'time' : st}}})
										sectors = db.sector_map.find({'pname' : query_hw['pname']})
										if sectors:
											for a in sectors:
												db.sector_map.update({'x' : a['x'] , 'y' : a['y']},{"$set" : {'pname' : pname, 'alliance' : alliance}})
										warps = db.warps.find({'player' : query_hw['pname']})
										if warps:
											for a in warps:
												db.warps.update({'player' : query_hw['pname']},{"$set" : {'player' : pname}})
									else:
										db.homeworlds.update({'_id' : query_hw['_id']}, {"$set" : {'last_online' : online}})
												
								else:
									db.homeworlds.insert({'pname' : pname, 'x' : x, 'y' : y, 'time' : st, 'type' : type, 'updates' : [], 'alias' : [], 'relation' : "", 'last_online' : online, 'score' : [], 'sector_count' : [], 'current_score' : 1, 'current_sectors' : 1, 'alliance' : ""})
							elif homeworld == "YES" and warp_gate_qty == 0:
								type = "HomeWorld"
								query_hw = db.homeworlds.find_one({'x' : x, 'y' : y})
								if query_hw:
									if query_hw['pname'] != pname:
										db.homeworlds.update({'_id' : query_hw['_id']}, {"$set" : {'pname' : pname, 'last_online' : online}})
										db.homeworlds.update({'_id' : query_hw['_id']}, {"$push" : {'alias' : {'Player' : query_hw['pname'], 'time' : st}}})
										sectors = db.sector_map.find({'pname' : query_hw['pname']})
										if sectors:
											for a in sectors:
												db.sector_map.update({'x' : a['x'] , 'y' : a['y']},{"$set" : {'pname' : pname, 'alliance' : alliance}})
										warps = db.warps.find({'player' : query_hw['pname']})
										if warps:
											for a in warps:
												db.warps.update({'player' : query_hw['pname']},{"$set" : {'player' : pname}})
									else:
										db.homeworlds.update({'_id' : query_hw['_id']}, {"$set" : {'last_online' : online}})
								else:
									db.homeworlds.insert({'pname' : pname, 'x' : x, 'y' : y, 'time' : st, 'type' : type, 'updates' : [], 'alias' : [], 'relation' : "", 'last_online' : online, 'score' : [], 'sector_count' : [], 'current_score' : 1, 'current_sectors' : 1, 'alliance' : ""})
							elif research_qty > 0:
								type = "Teching"
							elif star_ship_qty > 0:
								type = "Producer"
							elif warp_gate_qty > 0 and tcc_qty > 0:
								type = "WarpGate"
							elif star_ship_qty == 0 and research_qty == 0 and warp_gate_qty == 0 and defense_qty > 0:
								type = "Defense"
							else:
								type = "Empty"
							db.sector_map.update({'x' : x, 'y': y }, {"$set" : {'status' : "Player", 'size' : size, 'pname' : pname, 'type' : type, 'asp' : asp, 'sdi' : sdi, 'wada' : wada, 'corporate_factory' : corporate_factory, 'last_scan' : date, 'last_update' : st, 'dg1' : dg1, 'dg2' : dg2, 'dg3' : dg3, 'dg4' : dg4, 'dg5' : dg5, 'defense' : format(dmg, ",d")}})
							
							db.sector_map.update({'x' : x, 'y': y }, {"$set" : {'units' : [], 'products' : []}})
							db.sector_map.update({'x' : x, 'y': y }, {"$push" : {'units' : {'dagger' : dagger, 'dagger_mv' : dagger_mv, 'hydra' : hydra, 'hydra_mv' : hydra_mv, 'jackal' : jackal, 'jackal_mv' : jackal_mv, 'morningstar' : morningstar, 'morningstar_mv' : morningstar_mv, 'firefly' : firefly, 'firefly_mv' : firefly_mv, 'wyvern' : wyvern, 'wyvern_mv' : wyvern_mv, 'paladin' : paladin, 'paladin_mv' : paladin_mv, 'warlock' : warlock, 'warlock_mv' : warlock_mv, 'warlock_st' : warlock_st, 'scarab' : scarab, 'aesir' : aesir, 'aesir_mv' : aesir_mv, 'broadsword' : broadsword, 'broadsword_mv' : broadsword_mv }}})
							
							db.sector_map.update({'x' : x, 'y': y }, {"$push" : {'products' : {'tc_0106' : tc_0106, 'tc_1212' : tc_1212, 'tc_912' : tc_912 }}})
							
							db.sector_map.update({'x' : x, 'y' : y},{"$push": { 'updates' : {'player' : pname, 'source' : "scan", 'status' : "Player", 'time' : date, 'user' : user }}})
							db.homeworlds.update({'pname' : pname}, {"$set" : {'last_online' : online}})
						
							inserted +=1
							
					else:
						skipped +=1
				
					alliance = ""
					reactor = ""
					reactor_lvl = ""
					reactor_qty = 0
					tcc = ""
					tcc_lvl = ""
					tcc_qty = 0
					star_ship = ""
					star_ship_lvl = ""
					star_ship_qty = 0
					corporate_factory = "NO"
					ore = ""
					ore_lvl = ""
					ore_qty = 0
					crystal = ""
					crystal_lvl = ""
					crystal_qty = 0
					research = ""
					research_lvl = ""
					research_qty = 0
					population = ""
					population_lvl = ""
					population_qty = 0
					warp_gate = ""
					warp_gate_lvl = ""
					warp_gate_qty = 0
					defense = ""
					defense_lvl = ""
					defense_qty = 0
					sdi = "NO"
					asp = "NO"
					wada = "NO"
					dmg = 0
					dagger = 0
					dagger_mv = 0
					hydra = 0
					hydra_mv = 0
					jackal = 0
					jackal_mv = 0
					morningstar = 0
					morningstar_mv = 0
					firefly = 0
					firefly_mv = 0
					wyvern = 0
					wyvern_mv = 0
					paladin = 0
					paladin_mv = 0
					warlock = 0
					warlock_mv = 0
					warlock_st = 0
					scarab = 0
					aesir = 0
					aesir_mv = 0
					broadsword = 0
					broadsword_mv = 0
					sf_m44 = 0
					tc_0106 = 0
					tc_1212 = 0
					tc_912 = 0
					online = ""
					dg1 = 0
					dg2 = 0
					dg3 = 0
					dg4 = 0
					dg5 = 0
				elif debug == 1:
					# Print Sector Intel
					sector = sector.split(',')
					print """
						Date : %s
						X,Y : %d,%d
						Pname: %s
						Alliance : %s
						Size : %s
						Online : %s
						HomeWorld : %s
					""" %(date, int(sector[0]),int(sector[1]), pname, alliance, size, online, homeworld)
					print corporate_factory, sdi, asp, wada, dg1, dg2, dg3, dg4, dg5
					time.sleep(.5)
					# Print Building Data
					# print """
						# Corporate Factory : $r
						# SDI : %r
						# ASP : %r
						# WADA : %r
						# DG1 : %r
						# DG2 : %r
						# DG3 : %r
						# DG4 : %r
						# DG5 : %r
					# """ %(corporate_factory, sdi, asp, wada, dg1, dg2, dg3, dg4, dg5)
					dg1 = 0
					dg2 = 0
					dg3 = 0
					dg4 = 0
					dg5 = 0
					alliance = ""
					corporate_factory = "NO"
					sdi = "NO"
					asp = "NO"
					wada = "NO"
					
					
					
					
	return(inserted, skipped)
	
	
if __name__=="__main__":
	scanLog("scan.txt", "Xariec")