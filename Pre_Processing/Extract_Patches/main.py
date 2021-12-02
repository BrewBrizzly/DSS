# Script for extacting from the base patches
# All the patches that meet the requirement(s)

# Required lib 
from extact import extract_patches

def det_threshold(cutoff, dim):
	pixels = dim * dim 
	return cutoff * pixels 

def main():

	# Setting the required paths 
	path_to_patches = ''
	path_to_save = ''

	# Calculating the desired threshold 
	threshold = det_threshold(0.15, dim)

	# Extracting the pacthes and creating a list 
	extract_patches(path_to_patches, path_to_save, int(threshold))

if __name__ == '__main__':
	main()

