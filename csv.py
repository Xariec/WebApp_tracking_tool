import time
import datetime
import pymongo
db = pymongo.Connection('localhost', 27017).cc

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

#st is a timestamp of now in unicode


input_src = db.xariec.find() # the collection the intel was imported to. 

pname = "Xariec" # Player Name
type = "Friendly" # Relation with UWS
alliance = "United We Stand"
last_scan = st
last_update = st
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

for a in input_src:
	x = a['X']
	y = a['Y']
	size = a['Size']
	asp = a['ASP']
	sdi = a['SDI']
	wada = a['WADA']
	if asp >= 1:
		asp = "YES"
	else:
		asp = "NO"
		
	if sdi >= 1:
		sdi = "YES"
	else:
		sdi = "NO"
		
	if wada >= 1:
		wada = "YES"
	else:
		wada = "NO"
		
	print x,y, size, asp, sdi, wada
	
	db.sector_map.update({'x' : x, 'y': y }, {"$set" : {'status' : "Player", 'size' : size, 'pname' : pname, 'alliance' : alliance, 'type' : type, 'asp' : asp, 'sdi' : sdi, 'wada' : wada, 'defense' : format(dmg, ",d"), 'last_scan' : st, 'last_update' : st}}) # Updates sector
	
	db.sector_map.update({'x' : x, 'y': y }, {"$set" : {'units' : []}}) # clears previous units
	
	db.sector_map.update({'x' : x, 'y': y }, {"$push" : {'units' : {'dagger' : dagger, 'dagger_mv' : dagger_mv, 'hydra' : hydra, 'hydra_mv' : hydra_mv, 'jackal' : jackal, 'jackal_mv' : jackal_mv, 'morningstar' : morningstar, 'morningstar_mv' : morningstar_mv, 'firefly' : firefly, 'firefly_mv' : firefly_mv, 'wyvern' : wyvern, 'wyvern_mv' : wyvern_mv, 'paladin' : paladin, 'paladin_mv' : paladin_mv, 'warlock' : warlock, 'warlock_mv' : warlock_mv, 'warlock_st' : warlock_st, 'scarab' : scarab, 'aesir' : aesir, 'aesir_mv' : aesir_mv, 'broadsword' : broadsword, 'broadsword_mv' : broadsword_mv }}}) # sets all units to zero
	db.sector_map.update({'x' : x, 'y' : y},{"$push": { 'updates' : {'player' : pname, 'source' : "scan", 'status' : "Player", 'time' : st, 'user' : "Xariec" }}}) # shows were the update came from