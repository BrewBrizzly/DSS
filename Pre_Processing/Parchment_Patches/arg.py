# Loading the argument paths through sys

# Modules
import sys

def read():
	if len(sys.argv) != 2:
		fragment = ''
		print("Arguments wrong! \n"
			  "Arguments in format 'path fragment' 'path mask'")
		sys.exit(0)
	else:
		fragment = sys.argv[1]
	return fragment 	