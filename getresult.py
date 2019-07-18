#!/usr/local/bin/pythonw

import urllib2
import sys
import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
fb = client.fb   
odds = fb.odds

def connection(tries=0):
	link = 'https://bet.hkjc.com/football/getJSON.aspx?jsontype=results.aspx'
	try:
		htmltext = urllib2.urlopen(link).read()
		y = len(json.loads(htmltext))
		print ("connection success", y)
		return(htmltext)
	except Exception:
		if tries < sys.getrecursionlimit():
				return connection(tries+1)
		else:
			print ("finally connection failed")
			exit()



htmltext = connection()
am = json.loads(htmltext)[1]
z = len(am["matches"])

for i in range (0, z):
	matchIDinofficial = am["matches"][i]["matchIDinofficial"]
	matchDate = am["matches"][i]["matchDate"]
	h = am["matches"][i]["accumulatedscore"][1]["home"]	
	a = am["matches"][i]["accumulatedscore"][1]["away"]
	if (h>a):
		whowin = "H"
	elif (a>h):
		whowin = "A"
	else:
		whowin = "D"
	print h,a,whowin
	winodd = fb.odds.find_one({"matchIDinofficial" : matchIDinofficial},{"_id": 0, whowin: 1})[whowin]
	result = fb.odds.update({"matchIDinofficial": matchIDinofficial}, {"$set": {"win": whowin, "win_odd": winodd "flag": 'result'}}, upsert=True )
	#print D


# database = fb
# collection = odds
# matchDate
# matchIDinofficial
# hadodds {A, D, H}
# awayTeam {teamNameEN}
# homeTeam {teamNameEN}