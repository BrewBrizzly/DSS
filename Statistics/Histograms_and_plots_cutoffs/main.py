# Script for obtaining statistics on the distribution of patches 

# Libraries 
from Statistic import statistic

def main():

    # Defining the path to the lists 
    path = '/home/s3690970/Desktop/Bachelor_Project/DSS/Statistics/Lists_for_all_cutoffs/Lists/'

    # Initializing statistics object
    stc = statistic(path)

    # Create and save histogram for each list 
    stc.make_histogram()

    # Create one histogram containing the count
    stc.make_summary()


if __name__ == '__main__':
	main()
