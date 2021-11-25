# Counting, for each cutoff, the amount of patches and fragments 

# files 
from loop_patches import *

def main():

	# temporary list to track the number of patches, abd fragments, above a cutoff point, and the point itself 
	tmp_patches = []
	tmp_fragments = []
	tmp_cutoff = []

	# Reading the paths to fragment and performing the pre-processing steps 
	read('/data/p301438/IAAfragments_isolated_parchment_onlyColor-resized50/', tmp_patches, tmp_fragments, tmp_cutoff, 256)

if __name__ == '__main__':
	main()