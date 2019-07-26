#!/usr/local/bin/pythonw

import urllib2
import sys
import json
import logging
import datetime
from pymongo import MongoClient


logging.basicConfig(filename='logs',level=logging.DEBUG)

client = MongoClient('localhost', 27017)
fb = client.fb   
odds = fb.odds

def connection(tries=0):
	link = 'https://bet.hkjc.com/football/getJSON.aspx?jsontype=results.aspx'
	try:
		htmltext = urllib2.urlopen(link).read()
		am = json.loads(htmltext)[1]
		z = len(am["matches"])
		logging.info("[getresult] connection success at %s", datetime.datetime.now())
		return(am,z)
	except Exception:
		logging.info("[getresult] tries=%s", tries)
		if tries < sys.getrecursionlimit():
				return connection(tries+1)
		else:
			logging.info("[getresult] connection failed at %s", datetime.datetime.now())
			exit()

def writeDB(am,z):
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
		try:
			winodd = fb.odds.find_one({"matchIDinofficial" : matchIDinofficial},{"_id": 0, whowin: 1})[whowin]
			result = fb.odds.update({"matchIDinofficial": matchIDinofficial}, {"$set": {"win": whowin, "win_odd": winodd, "flag": 'result'}}, upsert=True )
			logging.info("[getresult] writeDB match %s and upated %s at %s", result.matched_count, result.modified_count, datetime.datetime.now())
		except:
			logging.info("[getresult] writeDB record %s not found", matchIDinofficial)

try:
	am,z = connection()
	writeDB(am,z)
except Exception as e:
	logging.exception("[getresult] connection failed"+repr(e)+"at %s", datetime.datetime.now())
	exit()



	#print D


# database = fb
# collection = odds
# matchDate
# matchIDinofficial
# hadodds {A, D, H}
# awayTeam {teamNameEN}
# homeTeam {teamNameEN}