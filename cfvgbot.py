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
import interpret
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

	if message.content.startswith('Hi bot!') and message.server == None:
		await client.send_message(message.author, 'Hey!')

	if message.content.startswith('vbot eval '):	
		def parse_eq(data):
			try:
				data = parse_space(data)
				data = parse_hgcc(data)
				data = interpret.parse(data)
			except:
				data =  "ERROR"
			return data

		def parse_hgcc(data):
			while True:
				s = data.find('!')
				if s != -1:
					e = data.find(" ",s+1)
					if e == -1: v = data[s:] #reached end of equation
					else: v = data[s:e]
					t = v.split(',')
					result = HGCC(int(t[2]),int(t[1]),int(t[0][1:]),int(t[3]),find=">=")
					data = data.replace(v,str(float(result)))
				else:
					break
			return data
		
		def parse_space(data):
			data = data.replace("AND",'&')
			data = data.replace("XOR",'^')
			data = data.replace("OR",'|')
			for i in ['&','|','^','+','-','*','/',')','(']:	data = data.replace(i,' '+i+' ')
			return data

		data = message.content[len('vbot eval '):].strip()
		result = parse_eq(data)
		await client.send_message(message.channel, '{} the result for {} is: \n{}'.format(message.author.mention,data,result))
		
	if message.content.startswith('vbot hgcc '):
		data = message.content[len('vbot HGCC '):].strip()
		t = data.split(' ')
		try:
			result = HGCC(int(t[2]),int(t[1]),int(t[0]),int(t[3]),find=t[4])
		except:
			result = '''ERROR. Enter command as: vbot hgcc a b c d f
	a:=Sample size
	b:=Possible successes
	c:=Population size
	d:=Number of successes
	f:=Available inputs (no quotes): '<' , '<=' , '>' , '>=' , '='
	'''
		await client.send_message(message.channel, '{} HGCC({},{},{},{},{})={}',message.author.mention,t[2],t[1],t[0],t[3],t[4],result)
	
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

client.run(token)