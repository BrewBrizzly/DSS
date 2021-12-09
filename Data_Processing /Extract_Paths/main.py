# Scripts for creating an array i, for cutoff i, 
# containing lists of fragments, where each fragment i
# contains the paths to the patches of that fragment i 

# Required libraries 
from Create_paths import * 

def main():
	
	path = '/projects/mdhali/BscProjects/Stephan/IAApatches_parchment_onlyColor-resized50/'
	ceate_path_structure(path)	

if __name__ == '__main__':
	main()