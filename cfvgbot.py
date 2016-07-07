# V-mundi bot
# -----------
# Author: Nanosmasher
# Date: 06/07/16
# Version: 0.1
# Features:
# - Hypergeometric Calculator
# TODO:
# - card images
# other shit

import logging
import discord
import asyncio #time/wait stuff
import math
from fractions import *
from Hyper_Calculator import * #Math stuff

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

	if message.content.startswith('Hi bot!'):
		await client.send_message(message.author, 'Hey!')

	if message.content.startswith('`'):	
		tmp = await client.send_message(message.channel, 'Calculating...')

		def parse_eq(data):
			tmp = data
			try:
				tmp = parse_hgcc(tmp)
				tmp = parse_ao(tmp)
			except:
				tmp =  "ERROR"
			return tmp
		
		def parse_ao(data):
			tmp = data
			while True:
				a = tmp.find('AND')
				o = tmp.find('OR')
				if a == -1 and o == -1: break #If neither operator was found
				if (a < o and a != -1) or o == -1 : # AND is found
					at = tmp.find('AND',a+1)
					ot = tmp.find('OR',a+1)
					if at == -1 and ot == -1: #No more found
						v = tmp.split('AND')
						r = float(v[0])*float(v[1])
						tmp = r
						break
					elif (at < ot and at != -1) or ot == -1: # AND is found
						v = tmp[:at].split('AND')
						r = float(v[0])*float(v[1])
						tmp = tmp.replace(tmp[:at],str(r))
					else:
						v = tmp[:ot].split('AND')
						r = float(v[0])*float(v[1])
						tmp = tmp.replace(tmp[:ot],str(r))
				else:
					at = tmp.find('AND',o+1)
					ot = tmp.find('OR',o+1)
					if at == -1 and ot == -1:
						v = tmp.split('OR')
						r = float(v[0])+float(v[1]) - float(v[0])*float(v[1])
						tmp = r
						break
					elif (at < ot and at != -1) or ot == -1: # AND is found
						v = tmp[:at].split('OR')
						r = float(v[0])+float(v[1]) - float(v[0])*float(v[1])
						tmp = tmp.replace(tmp[:at],str(r))
					else:
						v = tmp[:ot].split('OR')
						r = float(v[0])+float(v[1]) - float(v[0])*float(v[1])
						tmp = tmp.replace(tmp[:ot],str(r))
			return tmp
			
		def parse_hgcc(data):
			tmp = data
			while True:
				s = tmp.find('!')
				if s != -1:
					e = tmp.find(' ',s)
					if e == -1: v = tmp[s:] #if there is no space 
					else: v = tmp[s:e]
					t = v.split(',')
					result = HGCC(int(t[2]),int(t[1]),int(t[0][1:]),int(t[3]),find=">=")
					tmp = tmp.replace(v,str(float(result)))
				else:
					break
			return tmp
				
		
		data = message.content[len('"'):].strip()
		result = parse_eq(data)
		await client.edit_message(tmp, '{} the result for {}\n{}'.format(message.author.mention,data,result))
	
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

client.run(token)