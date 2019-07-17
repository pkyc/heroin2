#!/usr/local/bin/pythonw

import urllib2
import re
import string
import json
from pymongo import MongoClient
from bs4 import BeautifulSoup


client = MongoClient('localhost', 27017)
fb = client.fb   
odds = fb.odds

link = 'https://bet.hkjc.com/football/getJSON.aspx?jsontype=index.aspx'

try:
	htmlfile = urllib2.urlopen(link)
	htmltext = htmlfile.read()
	y = len(json.loads(htmltext))
	print ("connection success", y)
except:
	print ("connection failed")
	exit()

#print(json.loads(htmltext)[1])
for x in range (0, y):
	matchIDinofficial = json.loads(htmltext)[x]['matchIDinofficial']
	matchDate = json.loads(htmltext)[x]['matchDate']
	awayTeam = json.loads(htmltext)[x]['awayTeam']['teamNameEN']
	homeTeam = json.loads(htmltext)[x]['homeTeam']['teamNameEN']
	D = json.loads(htmltext)[x]['hadodds']['D'][4:]
	A = json.loads(htmltext)[x]['hadodds']['A'][4:]
	H = json.loads(htmltext)[x]['hadodds']['H'][4:]
	result = fb.odds.update({"matchIDinofficial": matchIDinofficial}, {"$set": {"matchDate": matchDate, "awayTeam": awayTeam, "homeTeam": homeTeam, "H": H, "D": D, "A": A, "flag": 'odd'}}, upsert=True )
	print D


# database = fb
# collection = odds
# matchDate
# matchIDinofficial
# hadodds {A, D, H}
# awayTeam {teamNameEN}
# homeTeam {teamNameEN}