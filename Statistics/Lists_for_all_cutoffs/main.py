# Counting, for each cutoff, the amount of patches and fragments 

# files 
from loop_patches import *

def main():

	# temporary list to track the number of patches
	tmp_patches = []

	# Reading the paths to fragment and performing the pre-processing steps 
	read('/data/p301438/IAApatches_parchment_onlyColor-resized50/', tmp_patches, 256)

if __name__ == '__main__':
	main()