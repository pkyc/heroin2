#!/usr/local/bin/pythonw

import urllib2
import re
import string
import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
fb = client.fb   
odds = fb.odds

link = 'https://bet.hkjc.com/football/getJSON.aspx?jsontype=results.aspx'

try:
	htmltext = urllib2.urlopen(link).read()
	y = len(json.loads(htmltext))
	print ("connection success", y)
except:
	print ("connection failed")
	exit()

am = json.loads(htmltext)[1]
z = len(am["matches"])

for i in range (0, z):
	matchIDinofficial = am["matches"][i]["matchIDinofficial"]
	matchDate = am["matches"][i]["matchDate"]
	h = am["matches"][i]["accumulatedscore"][1]["home"]	
	a = am["matches"][i]["accumulatedscore"][1]["away"]
	if (h>a):
		whowin = h
	elseif (a>h):
		whowin = a
	else
		whowin =d
	print h,a,whowin


	result = fb.odds.update({"matchIDinofficial": matchIDinofficial}, {"$set": {"win": win, "win_odd": [win].odd "flag": 'odd'}}, upsert=True )
	print D


# database = fb
# collection = odds
# matchDate
# matchIDinofficial
# hadodds {A, D, H}
# awayTeam {teamNameEN}
# homeTeam {teamNameEN}