import sys
import os
import Parser


def main():

	filename = sys.argv[1]
	if not os.path.isfile(filename):
		print("Error: " + filename + " does not exist.")
		exit(0)
	if not os.access(filename, os.R_OK):
		print("Error: " + filename + " access denied.")
		exit(0)

	with open(filename) as f:
		with open(filename+"_output", "w") as o:
			o.write(Parser.parse(f))
			o.close()
		f.close()

if __name__ == "__main__":
	main()