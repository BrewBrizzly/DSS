# Script for extacting from the base patches
# a list of paths of patches that meet the requirement
# This list is ordered on bins 
# Example: paths = [[path_i, path_j, path_..], [path_x, path_z, path_..], ...]
#		   bins  = [     bin_i               ,          bin_j           , ...] 
# Fragments that do not contain more than one patch are not included in the list


# Required lib 
from extract import *

# Determines the pixel threshold 
def det_threshold(cutoff, dim):
	pixels = dim * dim 
	return pixels * (cutoff / 100) 

def main():

	# Setting the required path 
	path_to_patches = '/projects/mdhali/BscProjects/Stephan/IAApatches_parchment_onlyColor-resized50/'

	# Calculating the desired threshold 
	threshold = det_threshold(15, 256)

	# Extracting the pacthes and creating a list 
	extract_patches(path_to_patches, int(threshold))

if __name__ == '__main__':
	main()

