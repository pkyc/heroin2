#!/usr/local/bin/pythonw

import urllib2
import json
import logging
import sys
import datetime
from pymongo import MongoClient

logging.basicConfig(filename='logs',level=logging.DEBUG)


client = MongoClient('localhost', 27017)
fb = client.fb   
odds = fb.odds

#link = 'https://bet.hkjc.com/football/getJSON.aspx?jsontype=index.aspx'

def connection(tries=0):
	logging.info("[getodd] connection start at %s", datetime.datetime.now())

	link = 'https://bet.hkjc.com/football/getJSON.aspx?jsontype=index.aspx'
	try:
		htmltext = urllib2.urlopen(link).read()
		y = len(json.loads(htmltext))
		logging.info("[getodd] connection success at %s", datetime.datetime.now())
		return(htmltext,y)
	except Exception:
		logging.info("[getodd] tries=%s", tries)

		if tries < sys.getrecursionlimit():
				return connection(tries+1)
		else:
			logging.info("[getodd] finally connection failed at %s", datetime.datetime.now())
			exit()


def writeDB(y):
	for x in range (0, y):
		matchIDinofficial = json.loads(htmltext)[x]['matchIDinofficial']
		matchDate = json.loads(htmltext)[x]['matchDate']
		awayTeam = json.loads(htmltext)[x]['awayTeam']['teamNameEN']
		homeTeam = json.loads(htmltext)[x]['homeTeam']['teamNameEN']
		D = json.loads(htmltext)[x]['hadodds']['D'][4:]
		A = json.loads(htmltext)[x]['hadodds']['A'][4:]
		H = json.loads(htmltext)[x]['hadodds']['H'][4:]
		result = fb.odds.update_one({"matchIDinofficial": matchIDinofficial}, {"$set": {"matchDate": matchDate, "awayTeam": awayTeam, "homeTeam": homeTeam, "H": H, "D": D, "A": A, "flag": 'odd'}}, upsert=True )
		logging.info("[getodd] writeDB match %s and upated %s at %s", result.matched_count, result.modified_count, datetime.datetime.now())
		#logging.info("writeDB %s, %s", result.upserted_id, result.raw_result)


try:
	htmltext,y = connection()
	writeDB(y)
except Exception as e:
	logging.exception("connection failed"+repr(e))
	exit()



# database = fb
# collection = odds
# matchDate
# matchIDinofficial
# hadodds {A, D, H}
# awayTeam {teamNameEN}
# homeTeam {teamNameEN}