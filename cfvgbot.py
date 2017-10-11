# V-mundi bot
# -----------
# Author: Nanosmasher
# Date: 05/09/16
# Version: 0.4
# Features:
# - Hypergeometric Calculator
# - card effects and images
# TODO:
# - vmundi decklists
# other shit

import logging
import discord
import asyncio #time/wait stuff
import math
import interpret
import text # words
from fractions import *
from Hyper_Calculator import * #Math stuff
import getcardinfo as fetch #card fetcher
import getepic as epic #EPIC card fetcher

token = "" #Create a text file named token.key and put your token in it
with open('token.key', 'r') as myfile:
    token = myfile.read().replace('\n', '')

client = discord.Client()
logging.basicConfig(level=logging.INFO)
control = {} # The servers and their respective owners

# Alice - July 6th at 09:46 EST
# preferrably I'd like it to parse as: "!5,8,49,1" and also take statements like "!5,4,49,1 OR 5,49,1"
# <<[1 - (CDF[HypergeometricDistribution[5,8,49],1] - PDF[HypergeometricDistribution[5,8,49],1]) ]
@client.event
async def on_message(m):
	if m.author == client.user:
		return

	tmc = m.content
	rep = ""

	# Admin/Owner only functions
	if m.author == control[m.server.id]:
		if m.content.startswith('vbot updatedb'):
			if tmc[14:] == "cfvg":
				print("updating cfvg database")
				print(str(fetch.updatedb(True)))
			elif tmc[14:] == "epic":
				print("updating epic database")
				print(str(epic.updatedb(True)))
			else:
				print("no database of that name. If you want vanguard type 'cfvg'. If you want EicTCG type 'epic' ")
			return
	
	# @everyone functions
	cards = 0
	while True:
		lead = tmc.find("[")
		if lead == -1: break
		lag = tmc.find("]",lead)
		if lag == -1: break
		cards += 1
		if cards > 5:
			await client.send_message(m.channel, "Maximum card limit reached.")
			break
		if tmc[lead+1:lead+2] == "":
			result = fetch.cardresult(tmc[lead+2:lag], True)
		else:
			result = fetch.cardresult(tmc[lead+1:lag], False)
		rep = await client.send_message(m.channel, result)
		tmc = tmc.replace(tmc[lead:lag+1],"")
	if cards: return

	if m.content == ('Hi bot!') and m.server == None:
		rep = await client.send_message(m.author, "Hey ^_^")

	if m.content == ('vbot'):
		rep = await client.send_message(m.channel, text.about)

	if m.content.startswith('!'):
		data = m.content[len('!'):].strip()
		if data[0:1] == "!":
			result = epic.cardresult(data[1:],True)
		else:
			result = epic.cardresult(data,False)
		rep = await client.send_message(m.channel, result)

	if m.content.startswith('vbot help'):
		data = m.content[len('vbot help'):].strip()
		if data == [] or m.content=="vbot help":
			tmp = "vbot help [*]\nDisplays information about the command. Commands:\n"
			for i in text.helping: tmp += i + "\n"
			rep = await client.send_message(m.channel, tmp)
		elif data in text.helping:
			rep = await client.send_message(m.channel, text.helping[data])
		else:
			rep = await client.send_message(m.channel, "No command found")

	if m.content.startswith('vbot eval'):
		data = m.content[len('vbot eval'):].strip()
		result = interpret.parse(data)
		rep = await client.send_message(m.channel, '{} the result for {} is: \n{}'.format(m.author.mention,data,result))
		
	if m.content.startswith('vbot hgcc'):
		data = m.content[len('vbot hgcc'):].strip()
		t = data.split(' ')
		try:
			result = HGCC(int(t[0]),int(t[1]),int(t[2]),int(t[3]),find=t[4])
		except:
			result = "ERROR"
		rep = await client.send_message(m.channel, '{} HGCC({},{},{},{},{})={}'.format(m.author.mention,t[2],t[1],t[0],t[3],t[4],result))
		
	if m.content.startswith('vbot quickodds'):
		data = m.content[len('vbot quickodds'):].strip()
		t = data.split(' ')
		try:
			result = quickodds(int(t[0]),int(t[1]),int(t[2]),int(t[3]))
		except:
			result = "ERROR"
		rep = await client.send_message(m.channel, '{} quickodds({},{},{},{})=\n{}'.format(m.author.mention,t[2],t[1],t[0],t[3],result))
		
	if m.content.startswith('vbot cascadeodds'):
		data = m.content[len('vbot cascadeodds'):].strip()
		t = data.split(' ')
		try:
			result = cascadeodds(int(t[0]),int(t[1]),int(t[2]))
		except:
			result = "ERROR"
		rep = await client.send_message(m.channel, '{} cascadeodds({},{},{})=\n{}'.format(m.author.mention,t[2],t[1],t[0],result))
	
	# Bot's response
	if rep != "":
		print("{} wrote:{}".format(m.author,m.content.encode("utf-8")))
		print('responded with {}'.format(rep.content.encode("utf-8")))
	
	
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	for c in client.servers:
		control[c.id] = c.owner

client.run(token)
