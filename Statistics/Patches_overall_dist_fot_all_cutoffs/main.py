# Counting, for each cutoff, the amount of patches and fragments 

# files 
from arg import *

def main():

	# temporary list to track the number of patches above a cutoff point, and the point intself 
	tmp_patches = []
	tmp_fragments = []
	tmp_cutoff = []

	# Reading the paths to fragment and performing the pre-processing steps 
	read('/data/p301438/IAAfragments_isolated_parchment_onlyColor-resized50/', tmp_patches, tmp_fragments, tmp_cutoff)

if __name__ == '__main__':
	main()