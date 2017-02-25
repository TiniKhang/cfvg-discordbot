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
	
def updatedb(quiet):
	import sys
	sys.setrecursionlimit(10000) #recursion limit are you kidding me?
	database = {}
	card = 0
	page = 1
	basic = re.compile('[^0-9a-zA-Z ]+') # remove for pretty database
	nextpage = True
	while nextpage:
		r = requests.post("http://cardfight.wikia.com/wiki/Category:Cards?page="+str(page))
		soup = BeautifulSoup(r.content, 'html.parser', from_encoding=r.encoding) #utf-8		
		table = soup.find_all("div", class_="mw-content-ltr")
		linkset = table[2].select("a")
		for link in linkset:
			name = basic.sub('',link.string).lower()  # remove for pretty database, keep name = link.string
			if name == "userxxtheprincexx": continue # User:XxThePrincexX
			if name.find("card gallery") != -1: continue # Card Gallery:
			if name.find("set gallery") != -1: continue # Set Gallery:
			card += 1
			database[name] = link["href"]
			if not quiet: print("registered: " + name )
		page += 1
		if not quiet: print("going to page {}".format(page) )
		if len(soup.find_all("span", class_="paginator-next disabled")): nextpage = False # Quit if there is no next page

	with open("vanguard.db", "wb") as file:
		pickle.dump(database,file)
		return(card)
	return(-1)

def fetchcard(page,info):
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
		
	img = soup.select(".cftable .image")
	i = img[0].get('href')
	i = i[:i.find("/revision")]

	if info:
		return("**{}**\n*{} <<{}>> {}*\n{}\n{}\n".format(f(" Name "),f(" Grade / Skill "),f(" Clan "),f(" Power "),e,i))
	else:
		return("{} (Use '[[!' for effect)\n".format(i))

def cardresult(text,info):
	d = searchdb(text,14)
	tmp = "Multiple Cards found (max 15 results):"
	if len(d) == 0:
		return("No results found")
	elif len(d) == 1: # match found
		for key in d: tmp = fetchcard(d[key],info)
		return(tmp)
	else:
		for key in d: tmp += d[key][6:].replace("_"," ") + "; "
		return(tmp[:-2])