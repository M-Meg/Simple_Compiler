import math
import os

OP_CODE ={"ADD":"18", "AND":"40", "COMP":"28", "DIV":"24", "J":"3C", "JEQ":"30", "JGT":"34", "JLT":"38", "JSUB":"48", \
"LDA":"00", "LDCH":"50", "LDL":"08", "LDX":"04", "MUL":"20", "OR":"44", "RD":"D8", "RSUB":"4C", "STA":"0C", "STCH":"54",\
 "STL":"14", "STSW":"E8", "STX":"10", "SUB":"1C", "TD":"E0", "TIX":"2C", "WD":"DC", "+JSUB":"48", "EXTREF":""}

SYMBOL_TABLE = {"XREAD":"000000", "XWRITE":"000000"}

def set_loc_counter(lines, out_file):

	for line in lines:	
		line = line.upper()
		line_sections = line.split("	")

		if line_sections[1] == "START":
			prog_name = line_sections[0]
			Start_add = format(int(line_sections[2][:-1]), '06x')
			loc_add = Start_add
			print(Start_add, "{0: <6}".format(prog_name), "{0: <5}".format(line_sections[1]), "{0: <6}".format(Start_add))
			output = Start_add + "\t" + "{0: <6}".format(prog_name) + "\t" + "{0: <5}".format(line_sections[1]) + "\t" + "{0: <6}".format(Start_add)+ "\n"
			out_file.write(output)
			
		elif line_sections[1] == "END":
			print(loc_add, "{0: <6}".format(line_sections[0]), "{0: <5}".format(line_sections[1]), "{0: <6}".format(Start_add))
			output = loc_add + "\t" + "{0: <6}".format(line_sections[0]) + "\t" + "{0: <5}".format(line_sections[1]) + "\t" + "{0: <6}".format(Start_add)+ "\n"
			out_file.write(output)
			prog_length = int(loc_add, 16) - int(Start_add, 16)
			return prog_length
			
		elif line_sections[1] == "RESW":
			print(loc_add, "{0: <6}".format(line_sections[0]), "{0: <5}".format(line_sections[1]), "{0: <6}".format(line_sections[2][:-1]))
			loc_add = format(int(line_sections[2])*3 + int(loc_add, 16), '06x')
			output = loc_add + "\t" + "{0: <6}".format(line_sections[0]) + "\t" + "{0: <5}".format(line_sections[1]) + "\t" + line_sections[2][:-1]+ "\n"
			out_file.write(output)

		elif line_sections[1] == "RESB":
			print(loc_add, "{0: <6}".format(line_sections[0]), "{0: <5}".format(line_sections[1]), "{0: <6}".format(line_sections[2][:-1]))
			loc_add = format(int(line_sections[2]) + int(loc_add, 16), '06x')
			output = loc_add + "\t" + "{0: <6}".format(line_sections[0]) + "\t" + "{0: <5}".format(line_sections[1]) + "\t" + line_sections[2][:-1]+ "\n"
			out_file.write(output)

		elif line_sections[1] == "BYTE":
			if line_sections[2][0] == "X":
				print(loc_add, "{0: <6}".format(line_sections[0]), "{0: <5}".format(line_sections[1]), "{0: <6}".format(line_sections[2][:-1]))
				loc_add = format(int(math.ceil(len(line_sections[2][2:-2])/2)) + int(loc_add, 16), '06x')
				output = loc_add + "\t" + "{0: <6}".format(line_sections[0]) + "\t" + "{0: <5}".format(line_sections[1]) + "\t" + line_sections[2][:-1]+ "\n"
				out_file.write(output)

			elif line_sections[2][0] == "C":
				print(loc_add, "{0: <6}".format(line_sections[0]), "{0: <5}".format(line_sections[1]), "{0: <6}".format(line_sections[2][:-1]))
				loc_add = format(int(len(line_sections[2][2:-2])) + int(loc_add, 16), '06x')
				output = loc_add + "\t" + "{0: <6}".format(line_sections[0]) + "\t" + "{0: <5}".format(line_sections[1]) + "\t" + line_sections[2][:-1]+ "\n"
				out_file.write(output)

		elif line_sections[1] == "WORD":
			print(loc_add, "{0: <6}".format(line_sections[0]), "{0: <5}".format(line_sections[1]), "{0: <6}".format(line_sections[2][:-1]))
			loc_add = format(int(loc_add, 16) + 3, '06x')
			output = loc_add + "\t" + "{0: <6}".format(line_sections[0]) + "\t" + "{0: <5}".format(line_sections[1]) + "\t" + line_sections[2][:-1] + "\n"
			out_file.write(output)

		elif line_sections[1] == "+JSUB":
			print(loc_add, "{0: <6}".format(line_sections[0]), "{0: <5}".format(line_sections[1]), "{0: <6}".format(line_sections[2][:-1]))
			loc_add = format(int(loc_add, 16) + 4, '06x')
			output = loc_add + "\t" + "{0: <6}".format(line_sections[0]) + "\t" + "{0: <5}".format(line_sections[1]) + "\t" + line_sections[2][:-1]+ "\n"
			out_file.write(output)

		elif line_sections[1] == "EXTREF":
			print(loc_add, "{0: <6}".format(line_sections[0]), "{0: <5}".format(line_sections[1]), "{0: <6}".format(line_sections[2][:-1]))
			loc_add = format(int(loc_add, 16), '06x')
			output = loc_add + "\t" + "{0: <6}".format(line_sections[0]) + "\t" + "{0: <5}".format(line_sections[1]) + "\t" + line_sections[2][:-1]+ "\n"
			out_file.write(output)

		else:
			print(loc_add, "{0: <6}".format(line_sections[0]), "{0: <5}".format(line_sections[1]), "{0: <6}".format(line_sections[2][:-1]))
			loc_add = format(int(loc_add, 16) + 3, '06x')
			output = loc_add + "\t" + "{0: <6}".format(line_sections[0]) + "\t" + "{0: <5}".format(line_sections[1]) + "\t" + line_sections[2][:-1]+ "\n"
			out_file.write(output)



def sym_table(lines, out_file):
	for line in lines[1:]:	
		line = line.upper()
		line_sections = line.split("	")

		if line_sections[1] != "      ":
			print("+++++++++++++++++++")
			print("+", line_sections[1], "|", line_sections[0], "+")
			SYMBOL_TABLE[line_sections[1].split()[0]] = line_sections[0]
	print("+++++++++++++++++++")



def sym_file(out_file):
	out_file.write("\n\n\n")
	out_file.write("++++++++++++++++++\n")
	out_file.write("+ SYMBOL TABLES  +\n")
	for k in SYMBOL_TABLE:
		out_file.write("++++++++++++++++++\n")
		out_file.write("+ " + "{0: <6}".format(k) + "| " + SYMBOL_TABLE[k] + " +\n")
	out_file.write("++++++++++++++++++\n")



def obj_code(lines, out_file, prog_length):
	header = ""
	for line in lines:	
		line_sections = line.split("	")
		print(line_sections[2])

		if line_sections[2] == "START":
				Start_add = line_sections[0]
				prog_name = line_sections[1]
				print(prog_name)
				header = "\n\nH." + "{0: <6}".format(prog_name) + "." + "{0: <6}".format(Start_add) + "."  + "\nT"
				out_file.write(line)
						
		elif line_sections[2] == "END  ":
			# print("END")
			header += "\nE." + Start_add
			out_file.write(line)

		elif line_sections[2] == "EXTREF  ":
			pass
			
		elif line_sections[2] == "RESW ":
			obj = "no obj. code"
			print(obj)
			if header[-1] == "\n" or header[-1] =="T":
				pass
			else:
				header += "\n"
			out_file.write("{0: <27}".format(line[:-1]) + "\t" + obj + "\n")

		elif line_sections[2] == "RESB ":
			obj = "no obj. code"
			print(obj)
			if header[-1] == "\n" or header[-1] =="T":
				pass
			else:
				header += "\n"
			out_file.write("{0: <27}".format(line[:-1]) + "\t" + obj + "\n")

		elif line_sections[2] == "BYTE ":
			if line_sections[3][0] == "X":
				obj = line_sections[3][2:-2]
				print(obj)
				header +=  "." + obj
				out_file.write("{0: <27}".format(line[:-1]) + "\t" + obj + "\n")

			elif line_sections[3][0] == "C":
				obj =  ''.join(str(format(ord(c),'x')) for c in line_sections[3][2:-2])
				print(obj)
				header +=  "." + obj
				out_file.write("{0: <27}".format(line[:-1]) + "\t" + obj + "\n")
					
		elif line_sections[2] == "WORD ":
			print(line_sections[3].split())
			try:
				obj = format(int(line_sections[3][:-1]), '06x')
			except ValueError:
				obj = SYMBOL_TABLE[line_sections[3].split()[0]]

			print(obj)
			header +=  "." + obj
			out_file.write("{0: <27}".format(line[:-1]) + "\t" + obj + "\n")

		elif line_sections[2] == "+JSUB  ":
			obj = "4B100000"
			print(obj)
			header +=  "." + obj
			out_file.write("{0: <27}".format(line[:-1]) + "\t" + obj + "\n")

		elif line_sections[2] == "EXTREF":
			pass

		else:
			# print(line_sections[2].split()[0])
			op = OP_CODE[line_sections[2].split()[0]]

			if line_sections[3][-3:-1] == ",X":
				sy = SYMBOL_TABLE[line_sections[3][:-3]]
				x = format(int(sy, 16) + 32768, '04x')
				obj = op + x
				print(obj)
				header +=  "." + obj
				out_file.write("{0: <27}".format(line[:-1]) + "\t" + obj + "\n")
			else:
				sy = SYMBOL_TABLE[line_sections[3][:-1]]
				obj = op + sy[2:]
				print(obj)
				header +=  "." + obj
				out_file.write("{0: <27}".format(line[:-1]) + "\t" + obj + "\n")

	out_file.write(header)


def check(lines):
	labels = list()
	for line in lines[1:]:
		line = line.upper()
		line_sections = line.split("	")

		if line_sections[0] != "":
			labels.append(line_sections[0]) 
			# print(line_sections[0])

	for line in lines[1:]:	
		line = line.upper()
		line_sections = line.split("	")
		Sic = ["RESB", "RESW", "BYTE", "WORD", "END"]

		try:
			op = OP_CODE[line_sections[1]]
		except KeyError:
			if line_sections[1] in Sic :
				pass
			else:
				return (1, line_sections[1])
		
		if line_sections[2][-3:-1] == ",X":
			label = line_sections[2][:-3]
		else:
			label = line_sections[2][:-1]

		if label.isalpha():
			# print(line_sections[2][:-1])
			if label in labels:
				pass 
			else:
				return (2, label)

	return (0, 0)




def sic_assembler(name):

	with open(name) as f:
		lines = f.readlines()
		status = (0, 0) #check(lines)
		f.close()

	if status[0] == 0:
		with open(name) as f:
			lines = f.readlines()
			with open(name+"pass1", "w") as fp1:
				prog_length = set_loc_counter(lines, fp1)
				fp1.close()
			f.close()
		print(prog_length)
		with open(name+"pass1", "r") as fp1:
			lines = fp1.readlines()
			sym_table(lines, fp1)
			fp1.close()


		with open(name+"pass1") as f:
			lines = f.readlines()
			with open(name+"pass2", "w") as fp2:
				obj_code(lines, fp2, prog_length)
				fp2.close()
			f.close()

		with open(name+"pass1", "a") as fp1:
			sym_file(fp1)
			fp1.close()


	elif status[0] == 1 :
		print(status[1], "is not a valid SIC instruction")

	elif status[0] == 2:
		print(status[1], "label is undefined")



def main():

	sic_assembler("test1_output.asm")	


main()
