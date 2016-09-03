import pickle
import urllib
import urllib.request as urllib2
import requests
from bs4 import BeautifulSoup
import re

def searchdb(s,maxitems):
	term =  re.sub('[^0-9a-zA-Z ]+','',s).lower()
	if term == "": return("No card provided")
	with open("vanguard.db", "rb") as file:
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

def db2txt():
	with open("vanguard.db", "rb") as file:
		database = pickle.load(file)
		with open("vanguard.txt", "wb") as f:
			for k,v in database.items():
				f.write((k + ": " + v + "\n").encode('utf-8'))
		return("Written to vanguard.txt")
	return("No database found or written")
	
def updatedb(confirm):
	if not confirm: return(0)
	import sys
	sys.setrecursionlimit(10000) #recursion limit are you kidding me?
	database = {}
	card = 0
	url = "/wiki/Category:Cards"
	basic = re.compile('[^0-9a-zA-Z ]+') # remove for pretty database
	while True:
		skip = False
		r = requests.post("http://cardfight.wikia.com"+url)
		soup = BeautifulSoup(r.content, 'html.parser', from_encoding=r.encoding) #utf-8
		next = soup.find_all(string="next 200")
		if not next:
			next = soup.find_all(string="previous 200")
			skip = True
		table = next[0].find_parent("div").select(".mw-content-ltr")[0]
		linkset = table.select("a")
		for link in linkset:
			name = basic.sub('',link.string).lower()  # remove for pretty database, keep name = link.string
			if name == "userxxtheprincexx": continue # User:XxThePrincexX
			if name.find("card gallery") != -1: continue # Card Gallery:
			if name.find("set gallery") != -1: continue # Set Gallery:
			card += 1
			database[name] = link["href"]
			#print("registered: " + str(link["href"].encode('utf-8')) )

		if skip: break
		url = next[0].parent["href"]
		

	with open("vanguard.db", "wb") as file:
		pickle.dump(database,file)
		return(card)
	return(-1)

def fetchcard(page):
	r = requests.post("http://cardfight.wikia.com"+page)
	soup = BeautifulSoup(r.content, 'html.parser', from_encoding=r.encoding)
	table = soup.select(".cftable .info-main table")
	def f(a):
		return(table[0].findAll("td",text = a)[0].next_sibling.text[1:-1])

	effect = soup.select(".cftable .info-extra .effect tr:nth-of-type(2) td")
	if effect:
		for br in effect[0].find_all("br"):
			br.replace_with("\n")
		e = effect[0].text[1:-1]
	else:
		e = "*No effect*"
	return("**{}**\n*{} <<{}>> {}*\n{}\n".format(f(" Name "),f(" Grade / Skill "),f(" Clan "),f(" Power "),e))
	
def cardresult(text):
	d = searchdb(text,14)
	tmp = "Multiple Cards found (max 15 results):"
	if len(d) == 0:
		return("No results found")
	elif len(d) == 1: # match found
		for key in d: tmp = fetchcard(d[key])
		return(tmp)
	else:
		for key in d: tmp += d[key][6:].replace("_"," ") + "; "
		return(tmp[:-2])