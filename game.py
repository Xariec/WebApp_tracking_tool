import web
import re
import pymongo
import time
import math
import users
from db_updates import *
import session
import mongo_utils
from session import MongoStore
import templates
from templates import render
import lang.en as lang
import forms
import pprint
import parse
import read_map
import scan_log
from bson.objectid import ObjectId

web.config.debug = False

db = pymongo.Connection('localhost', 27017).cc


mongo = MongoStuff()

urls = (
	'/','Index',
	'/login/','Login',
	'/logout/','Logout',
    '/register/', 'Register',
	'/ccPlayers/','ccPlayers',
	'/intelViewer/','intelViewer',
	'/dbInteractions/', 'dbInteractions',
	'/ccMap/', 'ccMap',
	'/upload/','upload',
	'/admin/','admin',
	'/collection/','collection',
	'/Xariec/', 'Xariec',
	
	)
  
app = web.application(urls, globals())
session = web.session.Session(app, MongoStore(db, 'sessions'))
users.collection = db.users
users.session = session

current_user = "blah"

class Index(object): 
	@users.login_required
	def GET(self):
		return render('home.html')

		


class Login(object):
	def GET(self):
		next = web.input(_method='GET').get(' next' , '/' )
		
		return render('login.html', next=next)
		
	def POST(self):
		st = time_stamp()
		post = web.input(_method='POST')
		errors = {}
		try:
			user = users.authenticate(post['username'], post['password'])
			if user:
				users.login(user)
				db.users.update({'username' : post['username']},{"$push" :{'updates' : {'time' : st, 'action' : "Login", 'info' : ""}}})
			else:
				errors['__all__'] = lang.AUTH_FAILURE
		except KeyError:
			errors['__all__'] = lang.AUTH_FAILURE
			
		if errors:
			return render('login.html', errors=errors, next=post.get('next'))
		else:
			# current_user = user
			return web.seeother(post.get('next' , '/' ))
			
			
class Register(object):
    def GET(self):
        return render('register.html')

    def POST(self):
        post = web.input(_method='POST')
        errors = {}
        username = forms.get_or_add_error(post, 'username', errors, lang.NO_FIELD_SUPPLIED('username'))
        password = forms.get_or_add_error(post, 'password', errors, lang.NO_FIELD_SUPPLIED('password'))
        password_again = forms.get_or_add_error(post, 'password_again', errors, lang.NO_FIELD_SUPPLIED('password again'))

        forms.validate(errors, 'password_again', lang.PASSWORDS_DONT_MATCH, lambda p,p2: p == p2, (password, password_again))

        if username is not None:
            forms.validate(errors, 'username', lang.FIELD_MUST_BE_LEN('Username', 3), lambda u: len(u) >= 3, (username,))
            forms.validate(errors, 'username', lang.USERNAME_TAKEN, lambda u: not bool(db.users.find_one({'username':u})), (username,))
        if password is not None:
            forms.validate(errors, 'password', lang.FIELD_MUST_BE_LEN('Password', 5), lambda p: len(p) >= 5, (password,))            
            
        if errors:
			return render('register.html', errors=errors)
        else:
            users.register(username=username, password=users.pswd(password), access=0)
            web.seeother('/login/')            

class Logout(object):
    def GET(self):
        users.logout()
        return web.seeother('/')
		

class collection(object):
	def GET(self):
		return web.seeother('/')
		
class collection_old(object):
	def GET(self):
		sectors = []
		count = 0
		collection = db.sector_map.find({'pname' : { "$in" : ["Corax", "Crazybonkers", "Deaths Advisor the Angry", "DEMENTED", "Fraya", "Henchman 21", "Lieutenant Xience", "pwnyxpress", "Sniffles", "Zapper"]}}).sort('last_update', -1).limit(50)
		for a in collection:
			if len(sectors) < 2000:
				if a['last_update'] != "":
					count +=1
					sectors.append((a))
				else:
					continue
			
		return render('collection.html', sectors = sectors, count = count)	
			
		
		
class Xariec(object):
	@users.login_required
	def GET(self):
		user = users.get_user()['username']
		if user == "Xariec":
			site_users = []
			query = db.users.find()
			for a in query:
				site_users.append((a))
				
			return render('xariec.html', site_users = site_users)
			
		
class intelViewer(object):
	@users.login_required
	def GET(self):
		user = users.get_user()['username']
		access = users.get_user()['access']
		if access >= 1:
			players = mongo.playerList(access)
			alliance = mongo.alliances(access)
			score_time = mongo.scoreTime()
			sector_time = mongo.sectorTime()
			return render('intelViewer.html', players = players, alliances = alliance, score_time = score_time, sector_time = sector_time, access = access)
		else:
			return web.seeother('/')
		
	def POST(self):
		st = time_stamp()
		access = users.get_user()['access']
		user = users.get_user()['username']
		if access == 1:
			post = web.input(_method='POST')
			if post['submit'] == "View Player":
				pname = post['player']
				players = mongo.playerList(access)
				hw = db.homeworlds.find_one({'pname': pname})
				check_sectors = db.sector_map.find({'pname' : pname}).limit(150)
				mongo.userUpdates(user, st,"View Player", pname)
				alliance = mongo.alliances(access)
				return render('player.html', access = access, sector_list = check_sectors, players = players, hw = hw, alliance = alliance)

			elif post['submit'] == "View Alliance":
				print post
				alliance = mongo.alliances(access)
				mongo.userUpdates(user, st,"View Alliance", post['alliance'])
				sectors = mongo.returnAlliance(post['alliance']).limit(300)
				return render('alliance.html', sectors = sectors, alliance = alliance)

			
			elif post['submit'] == "Compare Players":
				p1 = post['player1']
				p2 = post['player2']
				info = "%s,%s" %(p1,p2)
				mongo.userUpdates(user, st,"Compare Players", info)
				p1_sectors = []
				p2_sectors = []
				p1_query = db.sector_map.find({'status' : "Player", 'pname' : p1}).limit(150)
				p2_query = db.sector_map.find({'status' : "Player", 'pname' : p2}).limit(150)
				for a in p1_query:
					p1_sectors.append((a))
				for b in p2_query:
					p2_sectors.append((b))
				players = mongo.playerList(access)
				print "test", p1, p2
				return render('compare.html', players = players, p1 = p1_sectors, p2 = p2_sectors, player1 = p1, player2 = p2)
			
			elif post['submit'] == "Sector Intel":
				print post
				xy = str(post['xy'])
				xy = xy.replace('.',',')
				xy = xy.split(',')
				print xy
				x = xy[0]
				y = xy[1]
				info = "%d,%d" %(int(x),int(y))
				mongo.userUpdates(user, st,"View Sector", info)
				db.users.update({'username' : user},{"$push" :{'updates' : {'time' : st, 'action' : "View Sector", 'info' : info}}})
				sector_range = mongo.findRange(x,y)
				sector = mongo.findSector(x,y)
				players = mongo.playerList(access)
				return render('sector.html', sector = sector, players = players, sector_range = sector_range, access = access)
				
			elif post['submit'] == "Score Changes":
				print post
				time = post['score_time']
				mongo.userUpdates(user, st,"View Score", time)
				score_time = db.scoreKeeper.find()
				scores = db.scoreKeeper.find_one({'time' : time})
				return render('score.html', score_time = score_time, scores = scores)				
			elif post['submit'] == "Sector Changes":
				print post
				time = post['sector_time']
				mongo.userUpdates(user, st,"View Sector Count", time)
				sector_time = mongo.sectorTime()
				sectors = db.sectorKeeper.find_one({'time' : time})
				return render('sectors.html', sector_time = sector_time, sectors = sectors)
		
		
		if access >= 2:
			post = web.input(_method='POST')
			if post['submit'] == "View Player":
				pname = post['player']
				players = mongo.playerList(access)
				hw = db.homeworlds.find_one({'pname': pname})
				check_warps = db.warps.find({'player' : pname})
				check_sectors = db.sector_map.find({'pname' : pname})		
				map = db.sector_map.find({'pname' : pname})		
				mongo.userUpdates(user, st,"View Player", pname)
				alliance = mongo.alliances(access)
				return render('player.html', access = access, sector_list = check_sectors, players = players, hw = hw, alliance = alliance)
			
			elif post['submit'] == "Update Player":
				print post
				mongo.playerUpdate(post)
				players = mongo.playerList(access)
				pname = post['pname']
				hw = db.homeworlds.find_one({'pname': pname})
				check_warps = db.warps.find({'player' : pname})
				check_sectors = db.sector_map.find({'pname' : pname})		
				map = db.sector_map.find({'pname' : pname})		
				mongo.userUpdates(user, st,"View Player", pname)
				alliance = mongo.alliances(access)
				return render('player.html', access = access, sector_list = check_sectors, players = players, hw = hw, alliance = alliance)

			elif post['submit'] == "View Alliance":
				print post
				alliance = mongo.alliances(access)
				mongo.userUpdates(user, st,"View Alliance", post['alliance'])
				sectors = mongo.returnAlliance(post['alliance'])
				return render('alliance.html', sectors = sectors, alliance = alliance)

			
			elif post['submit'] == "Compare Players":
				p1 = post['player1']
				p2 = post['player2']
				info = "%s,%s" %(p1,p2)
				mongo.userUpdates(user, st,"Compare Players", info)
				p1_sectors = []
				p2_sectors = []
				p1_query = db.sector_map.find({'status' : "Player", 'pname' : p1})
				p2_query = db.sector_map.find({'status' : "Player", 'pname' : p2})
				for a in p1_query:
					p1_sectors.append((a))
				for b in p2_query:
					p2_sectors.append((b))
				players = mongo.playerList(access)
				print "test", p1, p2
				return render('compare.html', players = players, p1 = p1_sectors, p2 = p2_sectors, player1 = p1, player2 = p2)
			
			elif post['submit'] == "Sector Intel":
				print post
				xy = str(post['xy'])
				xy = xy.replace('.',',')
				xy = xy.split(',')
				print xy
				x = xy[0]
				y = xy[1]
				info = "%d,%d" %(int(x),int(y))
				mongo.userUpdates(user, st,"View Sector", info)
				db.users.update({'username' : user},{"$push" :{'updates' : {'time' : st, 'action' : "View Sector", 'info' : info}}})
				sector_range = mongo.findRange(x,y)
				sector = mongo.findSector(x,y)
				players = mongo.playerList(access)
				return render('sector.html', sector = sector, players = players, sector_range = sector_range, access = access)
				
			elif post['submit'] == "Score Changes":
				print post
				time = post['score_time']
				mongo.userUpdates(user, st,"View Score", time)
				score_time = db.scoreKeeper.find()
				scores = db.scoreKeeper.find_one({'time' : time})
				return render('score.html', score_time = score_time, scores = scores)				
			elif post['submit'] == "Sector Changes":
				print post
				time = post['sector_time']
				mongo.userUpdates(user, st,"View Sector Count", time)
				sector_time = mongo.sectorTime()
				sectors = db.sectorKeeper.find_one({'time' : time})
				return render('sectors.html', sector_time = sector_time, sectors = sectors)
				
			elif post['submit'] == "Update Sector":
				print post
				update_sector_intel = mongo.updateSector(post, user)
				x = int(post['x'])
				y = int(post['y'])
				info = "%d,%d" %(x,y)
				mongo.userUpdates(user, st,"Update Sector", info)
				sector_range = mongo.findRange(x,y)
				sector = mongo.findSector(x,y)
				players = mongo.playerList(access)
				return render('sector.html', sector = sector, players = players, sector_range = sector_range, access = access)
				
		else:
			return web.seeother('/')

			
class dbInteractions(object):
	@users.login_required
	def GET(self):
		user = users.get_user()['username']
		access = users.get_user()['access']
		if access > 1:
			players = mongo.playerList(access)
			sizes = mongo.sectorSizes()
			hw = mongo.homeworldList()
			return render('dbstuff.html', players = players, sizes = sizes, hw = hw)
		else:
			return web.seeother('/')	
	def POST(self):
		st = time_stamp()
		user = users.get_user()['username']
		access = users.get_user()['access']
		if access > 2:
			post = web.input(_method='POST')
			print post
			
			if post['submit'] == "hw":
				hw = post['hw']
				query = db.homeworlds.find_one({'pname' : hw})
				return render('hwUpdates.html', home = query)
			
			if post['submit'] == "List Sectors":
				if post['Intel'] == "Scanned Sectors":
					sectors = []
					mongo.userUpdates(user, st,"View Scanned Sectors", "")
					query = db.sector_map.find({'status' : "Player", 'last_scan' : {"$ne" : ""}})
					for a in query:
						sectors.append((a))
					
				if post['Intel'] == "Unscanned Sectors":
					sectors = []
					mongo.userUpdates(user, st,"View Non Scanned Sectors", "")
					query = db.sector_map.find({'status' : "Player", 'last_scan' :  ""}).limit(15000)
					for a in query:
						sectors.append((a))
						
				return render('scan_list.html', sectors = sectors)
			elif post['submit'] == "Map Sectors":
				mongo.userUpdates(user, st,"View Map", "")
				scanned = []
				unscanned = []
				scanned_query = db.sector_map.find({'status' : "Player", 'last_scan' : {"$ne" : ""}})
				unscanned_query = db.sector_map.find({'status' : "Player", 'last_scan' :  ""})
				for a in scanned_query:
					scanned.append((a))
				for b in unscanned_query:
					print b['x'],b['y']
					unscanned.append((b))
					
				return render('scan_map.html', scanned = scanned, unscanned = unscanned)

			elif post['submit'] == "View Cenvi":
				mongo.userUpdates(user, st,"List Cenvi Sectors", "")
				cenvi = db.sector_map.find({'status' : "Centrian"}).sort('size', -1)
				
				return render('cenvi.html', cenvi = cenvi)

			elif post['submit'] == "View Rebel":
				mongo.userUpdates(user, st,"List Rebel Sectors", "")
				rebel = db.sector_map.find({'status' : "Rebel"}).sort('size', -1).limit(3500)
				
				return render('rebel.html', rebel = rebel)
				
			elif post['submit'] == "by date":
				gt = "2015-"+post['date']+" 00:00:01"
				print gt
				query2 = db.sector_map.find({'status' : post['status'], 'last_scan' :  "", 'last_update' : {"$gte" : gt}})
				return render('bydate.html', query = query2)
			
			return web.seeother('/dbInteractions/')




				
class admin(object):
	@users.login_required
	def GET(self):
		st = time_stamp()
		user = users.get_user()['username']
		access = users.get_user()['access']
		if access >= 3:
			info = ""
			db.users.update({'username' : user},{"$push" :{'updates' : {'time' : st, 'action' : "View Users in Admin", 'info' : info}}})
			uws_users = mongo.userControl()
			return render('admin.html', access = uws_users)
		else:
			return web.seeother('/')
			
			
	def POST(self):
		st = time_stamp()
		user = users.get_user()['username']
		access = users.get_user()['access']
		if access >= 3:
			uws_users = mongo.userControl()
			post = web.input(_method='POST')
			new_access_level = int(post['lvl'])
			update_user = post['user']
			user_updated = db.users.find_one({'_id' : ObjectId(post['user'])})['username']
			info = "%s updated to lvl %d" %(user_updated, new_access_level)
			db.users.update({'username' : user},{"$push" :{'updates' : {'time' : st, 'action' : "Update Users in Admin", 'info' : info}}})
			new_access = mongo.updateAccess(update_user, new_access_level)
			return render('admin.html', access = uws_users)
	
		
		
class upload(object):
	@users.login_required
	def GET(self):
		user = users.get_user()['username']
		access = users.get_user()['access']
		if access > 2:
			map = db.map_time.find().sort('utime', -1).limit(1)
			for a in map:
				last_map = a['utime']
				
				print last_map
			return render('upload.html', last_map = last_map)
		else:
			return web.seeother('/')
	def POST(self):
		st = time_stamp()
		user = users.get_user()['username']
		access = users.get_user()['access']
		if access > 2:
			x = web.input(myfile={})
			print x['submit']
			if x['submit'] == "Upload Warps":
				info = ""
				db.users.update({'username' : user},{"$push" :{'updates' : {'time' : st, 'action' : "Upload Warps", 'info' : info}}})
				filedir = directory+'inbound_log/'
				# filedir = 'c:/Users/blbarn1x/Desktop/CC/inbound_log/'
				# filedir = '/var/lib/cc/inbound_log/' # change this to the directory you want to store the file in
				if 'myfile' in x: # to check if the file-object is created
					
					filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
					filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
					# print "supposed to read something", x.myfile.file.read()
					text_file_upload = x.myfile.file.read()
					fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
					fout.write(text_file_upload) # writes the uploaded file to the newly created file.
					fout.close() # closes the file, upload complete.
					the_file = filedir+filename
					parsing = parse.parse(the_file, user)
				return render('upload_completed.html', parsing = parsing)
			elif x['submit'] == "Upload Scans":
				info = ""
				db.users.update({'username' : user},{"$push" :{'updates' : {'time' : st, 'action' : "Upload Scans", 'info' : info}}})
				filedir = directory+'scans/'
				# filedir = 'c:/Users/blbarn1x/Desktop/CC/inbound_log/'
				# filedir = '/var/lib/cc/scans/' # change this to the directory you want to store the file in
				if 'myfile' in x: # to check if the file-object is created
					
					filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
					filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
					# print "supposed to read something", x.myfile.file.read()
					text_file_upload = x.myfile.file.read()
					fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
					fout.write(text_file_upload) # writes the uploaded file to the newly created file.
					fout.close() # closes the file, upload complete.
					the_file = filedir+filename
					parsing = scan_log.scanLog(the_file, user)
				return render('upload_completed.html', parsing = parsing)
				
			elif x['submit'] == "Upload Battles":
				info = ""
				db.users.update({'username' : user},{"$push" :{'updates' : {'time' : st, 'action' : "Upload Battles", 'info' : info}}})
				filedir = directory+'battles/'
				# filedir = 'c:/Users/blbarn1x/Desktop/CC/inbound_log/'
				# filedir = '/var/lib/cc/battles/' # change this to the directory you want to store the file in
				if 'myfile' in x: # to check if the file-object is created
					
					filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
					filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
					# print "supposed to read something", x.myfile.file.read()
					text_file_upload = x.myfile.file.read()
					fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
					fout.write(text_file_upload) # writes the uploaded file to the newly created file.
					fout.close() # closes the file, upload complete.
					the_file = filedir+filename
					parsing = mongo.bR(the_file, user)
				return render('upload_completed.html', parsing = parsing)
				
			elif x['submit'] == "Upload Score":
				info = ""
				db.users.update({'username' : user},{"$push" :{'updates' : {'time' : st, 'action' : "Upload Score", 'info' : info}}})
				filedir = directory+'score_uploads/'
				# filedir = 'c:/Users/blbarn1x/Desktop/CC/inbound_log/'
				# filedir = '/var/lib/cc/score_uploads/'
				if 'myfile' in x:
					
					filepath=x.myfile.filename.replace('\\','/')
					filename=filepath.split('/')[-1]
					text_file_upload = x.myfile.file.read()
					fout = open(filedir +'/'+ filename,'w') 
					fout.write(text_file_upload)
					fout.close() 
					the_file = filedir+filename
					parsing = mongo.scoreLog(the_file)
					
				return render('score_confirm.html', st = parsing)		
				
			elif x['submit'] == "Upload Sectors":
				info = ""
				db.users.update({'username' : user},{"$push" :{'updates' : {'time' : st, 'action' : "Upload Sector Counts", 'info' : info}}})
				filedir = directory+'sector_uploads/'
				# filedir = 'c:/Users/blbarn1x/Desktop/CC/inbound_log/'
				# filedir = '/var/lib/cc/sector_uploads/'
				if 'myfile' in x:
					
					filepath=x.myfile.filename.replace('\\','/')
					filename=filepath.split('/')[-1]
					text_file_upload = x.myfile.file.read()
					fout = open(filedir +'/'+ filename,'w') 
					fout.write(text_file_upload)
					fout.close() 
					the_file = filedir+filename
					parsing = mongo.sectorLog(the_file)
					
				return render('sector_confirm.html', st = parsing)	
				
			else:
				filedir = directory+"maps/"
				# filedir = '/var/lib/cc/maps/' # change this to the directory you want to store the file in
				if 'myfile' in x: # to check if the file-object is created
					info = ""
					db.users.update({'username' : user},{"$push" :{'updates' : {'time' : st, 'action' : "Upload Map", 'info' : info}}})
					filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
					print filepath
					user_time = x['utime']
					# filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
					filename= x['utime']+'.PNG' # splits the and chooses the last part (the filename with extension)
					print filename
					# print "supposed to read something", x.myfile.file.read()
					text_file_upload = x.myfile.file.read()
					fout = open(filedir +'/'+ filename,'wb') # creates the file where the uploaded file should be stored
					fout.write(text_file_upload) # writes the uploaded file to the newly created file.
					fout.close() # closes the file, upload complete.
					the_file = filedir+filename
					parsing = read_map.readMap(the_file, user_time, user)
				return render('img_upload_completed.html', parsing = parsing)

		else:
			raise web.seeother('/')
			
			
def time_stamp():
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	return st
	

if __name__=="__main__":
    web.internalerror = web.debugerror
    app.run()
