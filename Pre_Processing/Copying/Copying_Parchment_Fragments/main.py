# Copying the plates directory from source if plate contains
# Leather fragments.

# Defining globals
global source 
source = 'path'

global dest 
dest = 'path' 

global csv_path 
csv_path = 'path'


def main():

	# Reading the csv 
	csv_struct = read_csv(csv_path)

	# Actual copying of leather fragments 
	copy_fragments(source, dest, csv_struct)

if __name__ == '__main__':
	main()