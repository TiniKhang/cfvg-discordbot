# Does arithmetic operations with modificaitons:
# +,-,*,/,(,) work as they should
# & is the AND probability
# | is the OR probability
# ^ is the XOR probability

# bracket sorting alogrithm by me
# infix to postfix (reverse polish notation) using shunting-yard algorithim taken and modified from http://andreinc.net/2010/10/05/converting-infix-to-rpn-shunting-yard-algorithm/
# RPN evaluation taken and modified from https://rosettacode.org/wiki/Parsing/RPN_calculator_algorithm#Python

'''
Created on Oct 5, 2010

@author: nomemory
'''

#Associativity constants for operators
LEFT_ASSOC = 0
RIGHT_ASSOC = 1

#Supported operators
OPERATORS = {
	'+' : (0, LEFT_ASSOC),
	'-' : (0, LEFT_ASSOC),
	'*' : (5, LEFT_ASSOC),
	'/' : (5, LEFT_ASSOC),
	'&' : (5, LEFT_ASSOC),
	'|' : (10, LEFT_ASSOC),
	'^' : (10, LEFT_ASSOC)
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

def parse(input):
	while True:
		output = sorting(input)
		if len(output) > 0:
			i = output[len(output)][0]
			tmp = infix2rpn(input[i[0]:i[1]])
			tmp = rpn2num(tmp)
			input = input.replace(input[i[0]:i[1]],str(tmp))
		else: break
	return rpn2num(infix2rpn(input))


if __name__ == '__main__':
	input = " ( 1 + 2 ) * ( 3 / ( 2 + 2 ) ) - ( 5 + ( 6 - ( 5 + 5 ) )   )"
	output = parse(input)
	print(output)