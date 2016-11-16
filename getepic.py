import pickle
import urllib
import urllib.request as urllib2
import requests
from bs4 import BeautifulSoup
import re

def searchdb(s,maxitems):
	term =  re.sub('[^0-9a-zA-Z ]+','',s).lower()
	if term == "": return("No card provided")
	with open("epicww.db", "rb") as file:
		database = pickle.load(file)
		list = {}
		if term in database: return({term: database[term]})
		for i in database:
			if i.find(term) != -1:
				list[i] = database[i]
				maxitems -= 1
			if maxitems < 0: break
		return(list)
	return({})

def updatedb(quiet):
	basic = re.compile('[^0-9a-zA-Z ]+')
	database = {}
	r = requests.get("http://decks.epiccardgame.com/api/public/cards")
	jsonreq = r.json()
	for i in jsonreq:
		name = basic.sub('',i["name"]).lower()
		database[name] = i
		if not quiet: print("registered: " + name )
	with open("epicww.db", "wb") as file:
		pickle.dump(database,file)
		return(len(database))
	return(-1)

def cardresult(text,info):
	d = searchdb(text,14)
	tmp = "Multiple Cards found (max 15 results):"
	if len(d) == 0:
		return("No results found")
	elif len(d) == 1: # match found
		for name in d:
			x = d[name]
			if info:
				tmp = "**"+x["name"]+" ("+str(x["cost"])+")**\n" + "["
				if "offense" in x: str(x["offense"]) +" "
				tmp += x["faction_name"]+" "
				if "traits" in x: x["traits"].upper()+" "
				tmp += x["type_name"]+ " "
				if "defense" in x: str(x["defense"])
				tmp += "]\n" + x["text"]+"\n"
				if "discard" in x: tmp += "`" + x["discard"] + "`\n" 
				tmp += "http://decks.epiccardgame.com" + x["imagesrc"]+"\n"
			else:
				tmp = "http://decks.epiccardgame.com" + x["imagesrc"] + " (Put two '!' for text)\n"
		return(tmp)
	else:
		for key in d: tmp += d[key]["name"] + "; "
		return(tmp[:-2])