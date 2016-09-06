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

def updatedb(confirm):
	database = {}
	num = 0
	r = requests.post("http://www.epiccardgame.com/card-gallery/")
	soup = BeautifulSoup(r.content, 'html.parser', from_encoding=r.encoding)
	table = soup.select(".tablepress tbody tr")
	basic = re.compile('[^0-9a-zA-Z ]+')
	for card in table:
		name = card.find("td",class_="column-2").text
		reg = basic.sub('',name).lower()
		database[reg] = {
			"name": name,
			"img": card.a.get("href"),
			"cost": card.find("td",class_="column-3").text,
			"align": card.find("td",class_="column-4").text,
			"subtype": card.find("td",class_="column-10").text,
			"type": card.find("td",class_="column-5").text,
			"offense": card.find("td",class_="column-6").text,
			"defense": card.find("td",class_="column-7").text,
			"effect": card.find("td",class_="column-8").text
		}
		
		g = card.find("td",class_="column-9").text
		if len(g) > 0: database[reg]["effect"] += "\n `" + g + "`"
		
		num += 1
		print("Registered: " + name)
	with open("epicww.db", "wb") as file:
		pickle.dump(database,file)
		return(num)
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
				tmp = "**"+x["name"]+" ("+x["cost"]+")**\n" + "[" + x["offense"] +" "+ x["align"]+" "+x["subtype"]+" "+x["type"]+ " " + x["defense"] + "]\n" + x["effect"]+"\n"+x["img"]+"\n"
			else:
				tmp = x["img"] + " (Put two '!' for text)\n"
		return(tmp)
	else:
		for key in d: tmp += d[key]["name"] + "; "
		return(tmp[:-2])