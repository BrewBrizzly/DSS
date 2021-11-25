# Script for obtaining statistics on the distribution of patches 

# Libraries 
from Statistic import statistic

def main():

    # Defining the path to the patches 
    path = '/projects/mdhali/BscProjects/Stephan/IAApatches_parchment_onlyColor-resized50/'

    # Initializing statistics object
    stc = statistic(path, True)

    # Print the amount of unique patches
    stc.make_hist()

if __name__ == '__main__':
	main()