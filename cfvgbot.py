# V-mundi bot
# -----------
# Author: Nanosmasher
# Date: 14/07/16
# Version: 0.2
# Features:
# - Hypergeometric Calculator
# - card effects
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

token = "" #Create a text file named token.key and put your token in it
with open('token.key', 'r') as myfile:
    token=myfile.read().replace('\n', '')

client = discord.Client()
logging.basicConfig(level=logging.INFO)

# Alice - July 6th at 09:46 EST
# preferrably I'd like it to parse as: "!5,8,49,1" and also take statements like "!5,4,49,1 OR 5,49,1"
# <<[1 - (CDF[HypergeometricDistribution[5,8,49],1] - PDF[HypergeometricDistribution[5,8,49],1]) ]
@client.event
async def on_message(message):
	if message.author == client.user:
		return
		
	cards = 0
	tmc = message.content
	while True:
		lead = tmc.find("[[")
		if lead == -1: break
		lag = tmc.find("]]",lead)
		if lag == -1: break
		cards += 1
		if cards > 5:
			await client.send_message(message.channel, "Maximum card limit reached.")
			break
		print("{} searched for:{}".format(message.author,tmc[lead+2:lag].encode("utf-8")))
		msg = await client.send_message(message.channel, 'Searching...')
		result = fetch.cardresult(tmc[lead+2:lag])
		await client.edit_message(msg, result)
		tmc = tmc.replace(tmc[lead:lag+2],"")
		print('sent @{}:{}'.format(message.channel, result.encode("utf-8")))
	if cards: return

	if message.content == ('Hi bot!') and message.server == None:
		print("{} wrote:{}".format(message.author,message.content.encode("utf-8")))
		await client.send_message(message.author, "Hey ^_^")
		print('sent @{}:{}'.format(message.author, "Hey ^_^"))

	if message.content == ('vbot'):
		print("{} wrote:{}".format(message.author,message.content.encode("utf-8")))
		await client.send_message(message.channel, text.about)
		print('sent @{}:{}'.format(message.author, text.about))
	
	if message.content.startswith('vbot help'):
		print("{} wrote:{}".format(message.author,message.content.encode("utf-8")))
		data = message.content[len('vbot help'):].strip()
		print(data)
		if data == [] or message.content=="vbot help":
			tmp = "vbot help [*]\nDisplays information about the command. Commands:\n"
			for i in text.helping: tmp += i + "\n"
			await client.send_message(message.channel, tmp)
			print('sent @{}:{}'.format(message.author,tmp))
		elif data in text.helping:
			await client.send_message(message.channel, text.helping[data])
			print('sent @{}:{}'.format(message.author, text.helping[data]))
		else:
			await client.send_message(message.channel, "No command found")
			print('sent @{}:{}'.format(message.author, "No command found"))

	if message.content.startswith('vbot eval'):
		print("{} wrote:{}".format(message.author,message.content.encode("utf-8")))
		data = message.content[len('vbot eval'):].strip()
		result = interpret.parse(data)
		await client.send_message(message.channel, '{} the result for {} is: \n{}'.format(message.author.mention,data,result))
		print('sent @{}:{}'.format(message.author, '{} the result for {} is: \n{}'.format(message.author,data.encode("utf-8"),result)))
		
	if message.content.startswith('vbot hgcc'):
		print("{} wrote:{}".format(message.author,message.content.encode("utf-8")))
		data = message.content[len('vbot hgcc'):].strip()
		t = data.split(' ')
		try:
			result = HGCC(int(t[0]),int(t[1]),int(t[2]),int(t[3]),find=t[4])
		except:
			result = "ERROR"
		await client.send_message(message.channel, '{} HGCC({},{},{},{},{})={}'.format(message.author.mention,t[2],t[1],t[0],t[3],t[4],result))
		print('sent @{}:{}'.format(message.author, '{} HGCC({},{},{},{},{})={}'.format(message.author,t[2],t[1],t[0],t[3],t[4],result)))
		
	if message.content.startswith('vbot quickodds'):
		print("{} wrote:{}".format(message.author,message.content.encode("utf-8")))
		data = message.content[len('vbot quickodds'):].strip()
		t = data.split(' ')
		try:
			result = quickodds(int(t[0]),int(t[1]),int(t[2]),int(t[3]))
		except:
			result = "ERROR"
		await client.send_message(message.channel, '{} quickodds({},{},{},{})=\n{}'.format(message.author.mention,t[2],t[1],t[0],t[3],result))
		print('sent @{}:{}'.format(message.author, '{} quickodds({},{},{},{})=\n{}'.format(message.author,t[2],t[1],t[0],t[3],result)))
		
	if message.content.startswith('vbot cascadeodds'):
		print("{} wrote:{}".format(message.author,message.content.encode("utf-8")))
		data = message.content[len('vbot cascadeodds'):].strip()
		t = data.split(' ')
		try:
			result = cascadeodds(int(t[0]),int(t[1]),int(t[2]))
		except:
			result = "ERROR"
		await client.send_message(message.channel, '{} cascadeodds({},{},{})=\n{}'.format(message.author.mention,t[2],t[1],t[0],result))
		print('sent @{}:{}'.format(message.author,  '{} cascadeodds({},{},{})=\n{}'.format(message.author,t[2],t[1],t[0],result)))

		
		
		
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

client.run(token)