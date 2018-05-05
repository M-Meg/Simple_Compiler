import sys
import os
import Parser
import time


def main():

	filename = sys.argv[1]
	if not os.path.isfile(filename):
		print("Error: " + filename + " does not exist.")
		exit(0)
	if not os.access(filename, os.R_OK):
		print("Error: " + filename + " access denied.")
		exit(0)

	with open(filename) as f:
		with open(filename+"_output.asm", "w") as o:
			start = time.time()
			asm = Parser.parse(f)
			comp_time = time.time() - start
			o.write(asm)
			o.close()
		f.close()
	print("Compilation time: %s seconds" % comp_time)

if __name__ == "__main__":
	main()