# Script for obtaining statistics on the distribution of patches 

# Libraries 
from Statistic import statistic

def main():

    # Defining the path to the lists 
    path = '/Users/stephannijdam/Desktop/DSS/Statistics/Lists_for_all_cutoffs/Lists'

    # Initializing statistics object
    stc = statistic(path)

    # Create and save histogram for each list 
    stc.make_histogram()

    # Create one histogram containing the count
    # of each fragment with more than two patches 


if __name__ == '__main__':
	main()
