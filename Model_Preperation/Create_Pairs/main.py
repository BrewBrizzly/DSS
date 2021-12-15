# Creating the positive and negative pairs 

# Required libraries 
from pair import * 

def main():

	# Path to the array 
	path = '/projects/mdhali/BscProjects/Stephan/Model_data/Paths_15/Training_validating/Training-Validation.npy'

	# Creating the pairs
	create_pairs(path)

if __name__ == '__main__':
	main()