# Parses arithmetic operations with modificaitons:
# +,-,*,/,(,) work as they should
# & is the AND probability (right associativity)
# | is the OR probability (right associativity)
# ^ is the XOR probability (right associativity)

# sorting: mine. returns list containing level n brackets and indexs
# infix2rpn: infix to postfix (reverse polish notation) using shunting-yard algorithim taken and modified from http://andreinc.net/2010/10/05/converting-infix-to-rpn-shunting-yard-algorithm/
# parse: mine. base function calling everythin else.
# parse_pre: mine. adds a ton of spaces and replacements.
# parse_hgcc: mine. Convert ! => to numbers.
# parse_data: mine. Equation parser.
# rpn2num: RPN evaluation taken and modified from https://rosettacode.org/wiki/Parsing/RPN_calculator_algorithm#Python

import math
from fractions import *
from Hyper_Calculator import * #Math stuff

def sorting(data):
	dict = {}
	stack = []
	test = data.find('(')
	if test != -1:
		level = 0
		for i,c in enumerate(data):
			#print(dict)
			if c == '(':
				level = level + 1
				stack.append(i)
				if (level not in dict): dict[level] = list() #initilize
			elif c == ')':
				if (not level) or (len(stack) != level): return [] #) found before (
				dict[level].append([stack.pop(),i+1])
				level = level - 1
				#print(level)
		if level != 0: return [] # no closing bracket
		return dict
	else:
		return []

'''
Created on Oct 5, 2010

@author: nomemory
'''

#Associativity constants for operators
LEFT_ASSOC = 0
RIGHT_ASSOC = 1

#Supported operators
OPERATORS = {
	'+' : (5, LEFT_ASSOC),
	'-' : (5, LEFT_ASSOC),
	'*' : (10, LEFT_ASSOC),
	'/' : (10, LEFT_ASSOC),
	'&' : (0, LEFT_ASSOC),
	'|' : (0, LEFT_ASSOC),
	'^' : (0, LEFT_ASSOC)
}

#Test if a certain token is operator
def isOperator(token):
	return token in OPERATORS.keys()

#Test the associativity type of a certain token
def isAssociative(token, assoc):
	if not isOperator(token):
		raise ValueError('Invalid token: %s' % token)
	return OPERATORS[token][1] == assoc

#Compare the precedence of two tokens
def cmpPrecedence(token1, token2):
	if not isOperator(token1) or not isOperator(token2):
		raise ValueError('Invalid tokens: %s %s' % (token1, token2))
	return OPERATORS[token1][0] - OPERATORS[token2][0]

#Transforms an infix expression to RPN
def infix2rpn(tokens):
	tokens = tokens.split()
	out = []
	stack = []
	for token in tokens:
		if isOperator(token):
			while len(stack) != 0 and isOperator(stack[-1]):
				if (isAssociative(token, LEFT_ASSOC) and cmpPrecedence(token, stack[-1]) <= 0) or (isAssociative(token, RIGHT_ASSOC) and cmpPrecedence(token, stack[-1]) < 0):
					out.append(stack.pop())
					continue
				break
			stack.append(token)
		elif token == '(':
			stack.append(token)
		elif token == ')':
			while len(stack) != 0 and stack[-1] != '(':
				out.append(stack.pop())
			stack.pop()
		else:
			out.append(token)
	while len(stack) != 0:
		out.append(stack.pop())
	return out

def rpn2num(list):
	a=[]
	b={
		'+': lambda x,y: y+x,
		'-': lambda x,y: y-x,
		'*': lambda x,y: y*x,
		'/': lambda x,y: y/x,
		'&': lambda x,y: y*x,
		'|': lambda x,y: y+x-y*x,
		'^': lambda x,y: x*(1-y)+(1-x)*y
	}
	for c in list:
		if c in b: a.append(b[c](a.pop(),a.pop()))
		else: a.append(float(c))
	return a[0]

def parse_pre(data):
	data = data.replace("AND",'&')
	data = data.replace("XOR",'^')
	data = data.replace("OR",'|')
	data = data.replace("and",'&')
	data = data.replace("xor",'^')
	data = data.replace("or",'|')
	for i in ['&','|','^','+','-','*','/',')','(']:	data = data.replace(i,' '+i+' ')
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

def parse_data(input):
	while True:
		output = sorting(input)
		if len(output) > 0:
			i = output[len(output)][0]
			tmp = infix2rpn(input[i[0]:i[1]])
			tmp = rpn2num(tmp)
			input = input.replace(input[i[0]:i[1]],str(tmp))
		else: break
	return rpn2num(infix2rpn(input))

def parse(data):
	try:
		data = parse_pre(data)
		data = parse_hgcc(data)
		data = parse_data(data)
	except:
		data =  "ERROR"
	return data