import urllib
import urllib.request as urllib2
import requests
from bs4 import BeautifulSoup

def cardlist(s):
	#print("list:")
	payload = {
		"data[CardSearch][keyword]": "",
		"cmd": "search",
		"page": "1",
		"filter": "",
		"data[CardSearch][keyword_or]": "",
		"data[CardSearch][keyword_not]": "",
		"data[CardSearch][keyword_cardname]": "1",
		"data[CardSearch][keyword_text]": "0",
		"data[CardSearch][keyword_cardnumber]": "0",
		"data[CardSearch][keyword_tribe]": "0",
		"data[CardSearch][keyword_clan]": "0",
		"data[CardSearch][expansion]": "",
		"data[CardSearch][card_kind]": "",
		"data[CardSearch][country]": "",
		"data[CardSearch][grade_s]": "",
		"data[CardSearch][grade_e]": "",
		"data[CardSearch][skill_icon]": "",
		"data[CardSearch][power_s]": "",
		"data[CardSearch][power_e]": "",
		"data[CardSearch][shield_s]": "",
		"data[CardSearch][shield_e]": "",
		"data[CardSearch][critical_s]": "",
		"data[CardSearch][critical_e]": "",
		"data[CardSearch][card_trigger]": "",
		"data[CardSearch][show_page_count]": "10",
		"data[CardSearch][show_small]": "1",
		"button": "search"
	}
	payload["data[CardSearch][keyword]"] = s
	url = 'http://cf-vanguard.com/en/cardlist/cardsearch'
	r = requests.post(url,data=payload)
	soup = BeautifulSoup(r.content, 'html.parser', from_encoding=r.encoding) # ISO-8859-1
	l = soup.select("#searchResult-table-simple a")
	results = {}
	
	#with open("results.html", "wb") as file:
	#	file.write(r.content)
	
	for c in range(len(l)):
		name = l[c].text
		#print(name.encode('utf-8'))
		if not name in results: results[name] = l[c]["href"]
	return(results)

def cardinfo(link):
	page = urllib2.urlopen('http://cf-vanguard.com/en/cardlist' + link).read()
	soup = BeautifulSoup(page, 'html.parser', from_encoding="ISO-8859-1")
	table = soup.select("#cardDetail tr")
	n = table[0].find("th").find_next().string
	g = table[3].find("th").find_next().string
	c = table[4].find("th").find_next().string
	p = table[6].find("th").find_next().string
	e = table[8].find("th").find_next().string
	return("**{}**\n*Grade {} <<{}>> {} Power*\n{}\n".format(n,g,c,p,e))

def cardparse(s,result):
	d = {}
	#print("parse:")
	for item in result:
		name = item.lower()
		name = name.replace('\u2665','')
		name = name.replace('prism','ism')
		d[name] = result[item]
		#print(name.encode('utf-8'))
		
	if len(d) == 0:
		return("No results found")
	elif s in d: # exact match
		#print(d[s][1:])
		return(cardinfo(d[s][1:]))
	elif len(d) == 1: #ehhh...close enough
		(k, v), = d.items() # what the python is this
		return(cardinfo(v[1:]))
	else:
		tmp = "Multiple Cards found:"
		for key in result: tmp += key + "; "
		return tmp[:-2]

def cardget(s):
	s = s.lower()
	s = s.replace('\u2665','')
	s = s.replace('prism','ism')
	d = cardlist(s)
	#f = open("results.html", "rb")
	#soup = BeautifulSoup(f, 'html.parser', from_encoding="ISO-8859-1")
	#l = soup.select("#searchResult-table-simple a")
	#results = {}
	#print("list:")
	#for c in range(len(l)):
	#	name = l[c].text
	#	print(name.encode('utf-8'))
	#	if not name in results: results[name] = l[c]["href"]
	return(cardparse(s,d))
	
#print(cardget('').encode('utf-8')) #Test strings: Barcgal; Duo Petit Etoile, Peace; Leyte
#print(cardget('Duo Petit Etoile, Peac').encode('utf-8'))