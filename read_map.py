from PIL import Image
import time
import datetime
import pymongo
db = pymongo.Connection('localhost', 27017).cc



	
	
def readMap(the_file, user_time, user):
	map = []
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	im = Image.open(the_file)
	rgb_im = im.convert('RGB')
	rebel = 0
	cenvi = 0
	player = 0
	n = 940
	y=0
	sector_y = int(1)
	for c in range(0, n, 2):
		x=0
		sector_x = int(1)
		for d in range(0, n,2):
			r, g, b = rgb_im.getpixel((x,y))
			if r == 255 and g == 0 and b == 0:
				status = "Rebel"
			elif r == 198 and g == 226 and b == 255:
				status = "Centrian"
			elif r == 0 and g == 0 and b == 255:
				status = "Player"
			elif r == 0 and g == 0 and b == 0:
				status = "blank"
			query = db.sector_map.find_one({'x' : sector_x, 'y' : sector_y})['status']
			if query != status:
				db.sector_map.update({'x' : sector_x, 'y' : sector_y},{"$push": { 'updates' : {'player' : "", 'source' : "manual", 'status' : status, 'time' : st, 'user' : user }}})
				db.sector_map.update({'x' : sector_x, 'y' : sector_y}, {"$set" : {'status' : status, 'pname' : "", 'scan' : "", 'type' : "", 'asp' : "No", 'sdi' : "No", 'wada' : "No", 'alliance' : "", 'units' : [], 'last_scan' : "", 'defense' : "", 'last_update' : st, 'defense' : ""}})
				
				if status == "Rebel":
					rebel+=1
				elif status == "Centrian":
					cenvi+=1
				elif status == "Player":
					print "%d,%d became %s at %s" %(sector_x, sector_y, status, st)
					player+=1
			map.append((sector_x, sector_y, status))
			x+=2
			sector_x+=1
		y+=2
		sector_y+=1
		
	
	db.map_snapshots.insert({'map' : map, 'utime' : user_time})
	db.map_time.insert({'utime' : user_time})
	return(rebel,cenvi,player)
	
	
