import re


def tokenizer(line):

	if(re.match(r'(?i)PROGRAM', line)):
		token = re.match(r'(?i)program(.*)', line)
		return 1, token.group(1)

	elif(re.match(r'(?i)VAR', line)):
		token = re.match(r'(?i)var(.*)', line)
		return 2, token.group(1)

	elif(re.match(r'(?i)BEGIN', line)):
		token = re.match(r'(?i)BEGIN(.*)', line)
		return 3

	elif(re.match(r'(?i)END', line)):
		token = re.match(r'(?i)END(.*)', line)
		return (4,)

	elif(re.match(r'(?i)END.', line)):
		token = re.match(r'(?i)END.(.*)', line)
		return 5,

	elif(re.match(r'(?i)FOR', line)):
		token = re.match(r'(?i)FOR(.*)', line)
		return 6,

	elif(re.match(r'(?i)READ', line)):
		token = re.match(r'(?i)READ(.*)', line)
		return 7, token.group(1)

	elif(re.match(r'(?i)WRITE', line)):
		token = re.match(r'(?i)WRITE(.*)', line)
		return 8, token.group(1)

	elif(re.match(r'(?i)TO', line)):
		token = re.match(r'(?i)TO(.*)', line)
		return 9

	elif(re.match(r'(?i)DO', line)):
		token = re.match(r'(?i)DO(.*)', line)
		return 10

	elif(re.match(r'(?i);', line)):
		token = re.match(r';', line)
		return 11

	elif(re.match(r'(.*):=(.*)', line)):
		token = re.match(r'(.*):=(.*)', line)
		return 12, token.group(1), token.group(2)

	elif(re.match(r'(.*)\*(.*)', line)):
		token = re.match(r'(.*)\*(.*)', line)
		return 18, token.group(1), token.group(2)

	elif(re.match(r'\,', line)):
		token = re.match(r'\,', line)
		return 14

	elif(re.match(r'\(', line)):
		token = re.match(r'\(', line)
		return 15

	elif(re.match(r'\)', line)):
		token = re.match(r'\)', line)
		return 16

	elif(re.match(r'(?i)id', line)):
		token = re.match(r'(?i)id', line)
		return 17

	elif(re.match(r'(.*)\+(.*)', line)):
		token = re.match(r'(.*)\+(.*)', line)
		return 13, token.group(1), token.group(2)


def program(lines):

	token = re.match(r'(?i)PROGRAM(.*)(?i)VAR(.*?)(?i)BEGIN(.*)END.', lines)
	return token.group(1), token.group(2), token.group(3)


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