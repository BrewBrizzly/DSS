# Splitting the array of paths
# Into 80% Training/Validation and 
# 20% Testing

# Requiered library
from split import *

def main():

	# Path to the arrays to split
	path = '/projects/mdhali/BscProjects/Stephan/Sorted_paths/Arrays/'

	# Splitting the data in prefered in set manner
	split_data(path, 0.8, 0.2)

if __name__ == '__main__':
	main()