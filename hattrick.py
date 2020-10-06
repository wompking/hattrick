#An implementation of Hat Trick in Python.
#Hat Trick, and this interpreter, is by cyanidesDuality.

import sys
import re

if len(sys.argv) < 2:
	print("Usage: python3 hattrick.py <file>")
	sys.exit(-1)
debugging = False
if len(sys.argv) > 2:
	debugging = bool(sys.argv[2])

program = open(sys.argv[1]).read();

OPERATIONS                        = "+ - * / % ^ ? > < == != ! >= <= abs coerce find slice stdin len".split(" ")
OPERATIONSLENGTH = [int(a) for a in "2 2 2 2 2 2 3 2 2 2  2  1 2  2  1   2      2    3     0     1".split(" ") if a]

programsplit = [b for b in [a for a in program.split("\n") if a] if b[0] is not "#"]
programgrid = [a.split("=>") for a in programsplit]
programgrid = [[b.strip() for b in a] for a in programgrid]
print(programgrid)

variables = {}
hat_present = {}
present_hat = {}
reads = {}
pointer = 0

def isnum(s):
	return isinstance(s, int) or isinstance(s, float) 
def isstr(s):
	return isinstance(s, str)
def isbool(s):
	return isinstance(s, bool)
def isany(s):
	return isnum(s) or isstr(s) or isbool(s)

def strisnum(s):
	return len(re.findall(r"^((-?\d+\.?\d+)|(-?\d*\.?\d+))$", s)) == 1
def striszero(s):
	return len(re.findall(r"^(-?0+\.?0+)$", s)) == 1
def strisstr(s):
	return len(re.findall(r"(^\"([^\"]|\\\")*?\"$)|(^'([^']|\\')*?'$)", s)) == 1
def strisbool(s):
	return len(re.findall(r"^True$|^False$", s)) == 1
def strisany(s):
	return strisnum(s) or strisstr(s) or strisbool(s)


def getVal(g):
	global variables
	global hat_present
	global present_hat
	global reads
	global pointer
	global OPERATIONS
	global OPERATIONSLENGTH
	if g == "stdout":
		sys.exit("CANNOT INPUT FROM STDOUT")
	elif g not in variables.keys():
		sys.exit("UNKNOWN REFERENCE")
	elif g in hat_present.keys():
		sys.exit("CANNOT READ FROM ENTRANCE OF CALLCC PAIR")
	elif g in present_hat.keys():
		vs = variables.copy()
		v = vs[g]
		r = reads.copy()
		reads[g] = {"variables":vs, "hat_present":hat_present.copy(), "present_hat":present_hat.copy(), "pointer":pointer, "reads":r, "result":v}
		return v
	else:
		return variables[g]
def parseExpression(s):
	global variables
	global hat_present
	global present_hat
	global reads
	global pointer
	global OPERATIONS
	global OPERATIONSLENGTH
	L = s.split(" ")
	ptr = 0
	while ptr < len(L):
		#print("L",L)
		char = L[ptr]
		#print("char",char)
		if char in OPERATIONS:
			idx = OPERATIONS.index(char)
			opl = OPERATIONSLENGTH[idx]
			if ptr < opl:
				sys.exit("ERROR PARSING EXPRESSION [ "+s+" ]: NOT ENOUGH PARAMETERS FOR OPERATION " + char + " ON INDEX " + str(ptr))
			sli = L[ptr-opl:ptr]
			if any(map(lambda a: a in OPERATIONS, sli)):
				sys.exit("ERROR PARSING EXPRESSION [ "+s+" ]: SOMETHING BROKE??? SEE INDEX " + str(ptr))
			L = L[:ptr-opl]+[sli+[L[ptr]]]+L[ptr+1:]
			ptr -= opl
		ptr +=1
	if len(L) > 1:
		sys.exit("ERROR PARSING EXPRESSION [ "+s+" ]: CANNOT EVALUATE PARALLEL EXPRESSIONS")
	if isinstance(L[0], list):
		L = L[0]
	#print(L)
	return L

def evalExpression(tree):
	global variables
	global hat_present
	global present_hat
	global reads
	global pointer
	global OPERATIONS
	global OPERATIONSLENGTH
	#print(tree)
	if not isinstance(tree, list):
		if tree in OPERATIONS:
			#print("OPS")
			if tree == "stdin":
				return input("> ")
			else:
				return tree
		elif tree in variables.keys():
			return getVal(tree)
		else:
			if strisany(tree):
				return eval(tree)
			else:
				sys.exit("UNKNOWN VARIABLE REFERENCE: "+tree)
			return tree
		return tree
	elif len(tree) == 1:
		return evalExpression(tree[0])
	else:
		L = [evalExpression(i) for i in tree]
		#print(L)
		valOut = None
		if L[-1] == "+":
			if isnum(L[0]) and isnum(L[1]) or isstr(L[0]) and isstr(L[1]):
				return L[0] + L[1]
			elif isbool(L[0]) and isbool(L[1]):
				return L[0] or L[1]
			else:
				sys.exit("ERROR EVALUATING EXPRESSION "+str(L)+" : WRONG TYPES FOR OPERATOR +")
		elif L[-1] == "-":
			if isnum(L[0]) and isnum(L[1]):
				return L[0] - L[1]
			elif isbool(L[0]) and isbool(L[1]):
				return L[0] and not L[1]
			else:
				sys.exit("ERROR EVALUATING EXPRESSION "+str(L)+" : WRONG TYPES FOR OPERATOR -")
		elif L[-1] == "*":
			if isnum(L[0]) and isnum(L[1]):
				return L[0] * L[1]
			elif isstr(L[0]) and isnum(L[1]):
				return L[0] * L[1]
			elif isbool(L[0]) and isbool(L[1]):
				return L[0] and L[1]
			else:
				sys.exit("ERROR EVALUATING EXPRESSION "+str(L)+" : WRONG TYPES FOR OPERATOR *")
		elif L[-1] == "/":
			if isnum(L[0]) and isnum(L[1]):
				if iszero(L[0]) and iszero(L[1]):
					return "INDETERMINATE"
				elif iszero(L[1]):
					return "UNDEFINED"
				else:
					return L[0] / L[1]
			else:
				sys.exit("ERROR EVALUATING EXPRESSION "+str(L)+" : WRONG TYPES FOR OPERATOR /")
		elif L[-1] == "%":
			if isnum(L[0]) and isnum(L[1]):
				return L[0] % L[1]
			else:
				sys.exit("ERROR EVALUATING EXPRESSION "+str(L)+" : WRONG TYPES FOR OPERATOR %")
		elif L[-1] == "^":
			if isnum(L[0]) and isnum(L[1]):
				return L[0] ** L[1]
			elif isbool(L[0]) and isbool(L[1]):
				return L[0] ^ L[1]
			else:
				sys.exit("ERROR EVALUATING EXPRESSION "+str(L)+" : WRONG TYPES FOR OPERATOR ^")
		elif L[-1] == "?":
			if isbool(L[2]):
				return L[0] if L[2] else L[1]
			else:
				sys.exit("ERROR EVALUATING EXPRESSION "+str(L)+" : WRONG TYPES FOR OPERATOR ?")
		elif L[-1] == ">":
			if isnum(L[0]) and isnum(L[1]):
				return L[0] > L[1]
			else:
				sys.exit("ERROR EVALUATING EXPRESSION "+str(L)+" : WRONG TYPES FOR OPERATOR >")
		elif L[-1] == "<":
			if isnum(L[0]) and isnum(L[1]):
				return L[0] < L[1]
			else:
				sys.exit("ERROR EVALUATING EXPRESSION "+str(L)+" : WRONG TYPES FOR OPERATOR <")
		elif L[-1] == "==":
			return L[0] == L[1]
		elif L[-1] == "<=":
			if isnum(L[0]) and isnum(L[1]):
				return L[0] <= L[1]
			else:
				sys.exit("ERROR EVALUATING EXPRESSION "+str(L)+" : WRONG TYPES FOR OPERATOR <=")
		elif L[-1] == ">=":
			if isnum(L[0]) and isnum(L[1]):
				return L[0] >= L[1]
			else:
				sys.exit("ERROR EVALUATING EXPRESSION "+str(L)+" : WRONG TYPES FOR OPERATOR >=")
		elif L[-1] == "!=":
			return L[0] != L[1]
		elif L[-1] == "!":
			if isbool(L[0]):
				return not L[0]
			else:
				sys.exit("ERROR EVALUATING EXPRESSION "+str(L)+" : WRONG TYPE FOR OPERATOR !")
		elif L[-1] == "abs":
			if isnum(L[0]):
				return abs(L[0])
			else:
				sys.exit("ERROR EVALUATING EXPRESSION "+str(L)+" : WRONG TYPE FOR OPERATOR abs")
		elif L[-1] == "coerce":
			if isbool(L[1]):
				return True if L[0] else False
			elif isstr(L[1]):
				return str(L[0])
			elif isnum(L[1]):
				if isbool(L[0]):
					return 0 if L[0] else 1
				elif isstr(L[0]):
					try:
						test = eval(L[0])
					except SyntaxError:
						return L[0]
					if isnum(test):
						return test
					else:
						return L[0]
				elif isnum(L[0]):
					return L[0]
			else:
				sys.exit("ERROR EVALUATING EXPRESSION "+str(L)+" : WRONG TYPES FOR OPERATOR coerce")
		elif L[-1] == "find":
			if isstr(L[0]) and isstr(L[1]):
				return L[0].find(L[1])
			else:
				sys.exit("ERROR EVALUATING EXPRESSION "+str(L)+" : WRONG TYPES FOR OPERATOR find")
		elif L[-1] == "slice":
			if isnum(L[0]) and isnum(L[1]) and isstr(L[2]):
				return L[2][L[0]:L[1]]
			else:
				sys.exit("ERROR EVALUATING EXPRESSION "+str(L)+" : WRONG TYPES FOR OPERATOR slice")
		elif L[-1] == "len":
			if isstr(L[0]):
				return len(L[0])
			else:
				sys.exit("ERROR EVALUATING EXPRESSION "+str(L)+" : WRONG TYPES FOR OPERATOR len")

def valWrite(w,v):
	global variables
	global hat_present
	global present_hat
	global reads
	global pointer
	global OPERATIONS
	global OPERATIONSLENGTH
	if w in hat_present.keys():
		if hat_present[w] in reads.keys():
			k = reads[hat_present[w]].copy()
			if k["result"] == v:
				pass
			else:
				variables = k["variables"]
				hat_present = k["hat_present"]
				present_hat = k["present_hat"]
				pointer = k["pointer"]-1
				reads = k["reads"]
				variables[hat_present[w]] = v
		else:
			variables[w] = v
	else:
		variables[w] = v

while pointer < len(programgrid):
	line = programgrid[pointer]
	if debugging:
		print("\n\n")
		print("line",line)
		print("variables",variables)
		print("",hat_present)
		print("",present_hat)
		print("reads",reads)
		print("pointer",pointer)
		input("Press any key to continue. \n>")
		print("\n\n")
	value = None
	if line[0] == '':
		pass
	else:
		value = evalExpression(parseExpression(line[0]))
	if line[1] == "stdout":
		print(value)
	elif line[1] == "stdin":
		sys.exit("CANNOT WRITE TO STDIN")
	elif len(re.findall(r"^\[[^|]+?\|[^|]+?\]$", line[1])) == 1 and value == None:
		L = line[1].split("|")
		L = [L[0][1:], L[1][:-1]]
		hat_present[L[0]] = L[1]
		present_hat[L[1]] = L[0]
		variables[L[0]] = None
		variables[L[1]] = None
	else:
		valWrite(line[1],value)
	pointer += 1
