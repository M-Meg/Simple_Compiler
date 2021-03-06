import Tokenizer
import re
import sys
import time


IDs = list()
ra = ""


def parse(fl):

	lines = fl.read().replace("\n", "")
	name, id_list, stmt_list = Tokenizer.program(lines)

	header = name.strip() + "\tSTART\t0"
	if(re.match(r'(.*)(?i)READ(.*)', stmt_list) and re.match(r'(.*)(?i)WRITE(.*)', stmt_list)):
		header += "\n \tEXTREF\tXREAD, XWRITE"

	elif(re.match(r'(.*)(?i)READ(.*)', stmt_list)):
		header += "\n \tEXTREF\tXREAD"

	elif(re.match(r'(.*)(?i)WRITE(.*)', stmt_list)):
		header += "\n \tEXTREF\tXWRITE"

	header += var(id_list)

	return header + statments(stmt_list) + "\n\tEND\t0000"


def var(var):
	
	# print(var)
	global IDs
	var = var.split(",")
	s = ""
	for i in var:
		if(i):
			IDs.append(str(i).strip())
			s += "\n"+ str(i).strip() + "\tRESW\t1"

		else:
			print("Syntax Error: Variables declaration ','")
			exit(0)
	return s


def statments(stmts):

	# print("Stmt_list: " + stmts)
	if(";" in stmts):	
		var = re.match(r'(.*?);(.*)', stmts)
		if(Tokenizer.tokenizer(var.group(1))[0] == 6):
			fv = re.match(r'(?i)FOR(.*)DO(.*?)END;(.*)', stmts)
			return for_stmt(fv.group(1), fv.group(2)) + statments(fv.group(3))

		if(var.group(2)):
			return statments(var.group(1)) + statments(var.group(2))

		else:
			return statment(var.group(1))

	else:
		return statment(stmts)


def statment(stmt):

	token = Tokenizer.tokenizer(stmt.strip())
	# print(token)
	if(token):
		if(token[0] == 7):
			return read(token)

		elif(token[0] == 8):
			return write(token)

		elif(token[0] == 12):
			return assign(token[1:])

	else:
		print("Syntax Error: " + stmt)
		exit(0)


def for_stmt(cond, body):

	cond = re.match(r'(.*):=(.*)(?i)TO(.*)', cond)

	t = re.match(r'(?i)BEGIN(.*)', body.strip())

	try:
		if(t.group(1)):
			# print("BEG: " + t.group(1))
			r = statments(t.group(1).strip())
	except AttributeError:
		r = statments(body.strip())
			
	return "\n" + cond.group(1).strip() + "\tLDX\t" + factor(cond.group(2).strip()) \
	+"\n" + cond.group(1).strip() + "LOOP" + r[1:] \
	+"\n \tTIX\t" + factor(cond.group(3).strip()) \
	+"\n \tJLT\t" + cond.group(1).strip() + "LOOP"


def read(id):

	var = re.match(r'\((.*)\)', id[1])
	if(var):
		s = "\n \t+JSUB\tXREAD\n \tWORD\t" + str(len(var.group(1).split(",")))
		for i in var.group(1).split(","):
			s += "\n \tWORD\t"+ str(i).strip()
		return s
	else:
		print("Syntax Error: missing bracet '(' ')' in READ Statment")
		exit(0)


def write(id):
	var = re.match(r'\((.*)\)', id[1])
	if(var):
		s = "\n \t+JSUB\tXWRITE\n \tWORD\t" + str(len(var.group(1).split(",")))
		for i in var.group(1).split(","):
			s += "\n \tWORD\t"+ str(i).strip()
		return s
	else:
		print("Syntax Error: Missing bracet '(' ')' in WRITE Statment")
		exit(0)


def factor(f):

	if(id(f)):
		return f
	
	elif(f.isnumeric()):
		return "#" + f

	else:
		return exp(f)


def exp(e):

	t = Tokenizer.tokenizer(e)
	print(t)
	if(t):
		if(t[0] == 18):
			return mul(factor(t[1].strip()), factor(t[2].strip()))

		elif(t[0] == 13):
			return add(factor(t[1].strip()), factor(t[2].strip()))

	else:
		print("Syntax Error: '" + e.strip() + "' Unvalid Expression")
		exit(0)


def assign(a):

	if(id(a[0].strip())):
		return exp(a[1]) + "\n \tSTA\t" + a[0].strip()
	else:
		print("Error: Variable '" + a[0].strip() + "'' is not defined.")
		exit(0)


def id(i):

	global IDs
	if(i in IDs):
		return True
	else:
		return False


def add(a, b):

	global ra
	if(ra == a):
		ra = ""
		return "\n \tADD\t" + b

	elif(ra == a):
		ra = ""
		return "\n \tADD\t" + a

	else:
	 return getA(a) + add(a, b)


def mul(a, b):

	global ra
	if(ra == a):
		ra = ""
		return "\n \tMUL\t" + b

	elif(ra == a):
		ra = ""
		return "\n \tMUL\t" + a

	else:
	 return getA(a) + mul(a, b)


def getA(a):
	global ra
	ra = a
	return "\n \tLDA\t" + a


# IDs = ["a", "b", "c"]
# print(statments("FOR i := 1 to 100 DO BEGIN READ(V);a:= a + b; END;WRITE(sum);a := b + 2"))


# PROGRAM 1
# VAR 2
# BEGIN 3
# END 4
# END. 5
# FOR 6
# READ 7
# WRITE 8
# TO 9
# DO 10
# ; 11
# := 12
# + 13
# , 14
# ( 15
# ) 16
# id 17
# * 18