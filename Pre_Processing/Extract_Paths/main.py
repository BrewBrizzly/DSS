# Scripts for creating lists of paths for each cutoff 
# Followingly these paths are passed to create plots 
# and a summary

# Required libraries 
from Create_paths import * 

def main():
	
	path = '/projects/mdhali/BscProjects/Stephan/IAApatches_parchment_onlyColor-resized50/'
	ceate_paths(path)	

if __name__ == '__main__':
	main()