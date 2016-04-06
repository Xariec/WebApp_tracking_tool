import pymongo
import re

db = pymongo.Connection('localhost', 27017).cc


query = db.sector_map.find({'updates' : {"$ne" : ""}})
scorp = 0
xariec = 0
brew = 0
bitz = 0
jarvel = 0




for a in query:
	test = str(a['updates'])
	if re.search(r"Xariec", test):
		xariec +=1
	if re.search(r"Scorpion", test):
		scorp +=1
	if re.search(r"Jarvel", test):
		jarvel +=1
	if re.search(r"BrewMSTR", test):
		brew += 1
	if re.search(r"thebitz1", test):
		bitz += 1


print "Scorp: ", scorp
print "Xariec: ", xariec
print "Brew: ", brew
print "Jarvel: ", jarvel
print "Bitz: ", bitz	
