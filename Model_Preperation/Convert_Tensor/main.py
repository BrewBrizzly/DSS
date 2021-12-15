# Convert the array of paths to array 
# of tensors

# Required library
from tensor import *


def main():

	# Paths of array to be converted
	pathx = '/projects/mdhali/BscProjects/Stephan/Model_data/Paths_15/Training_validating/Paired/input_x.npy'
	pathy = '/projects/mdhali/BscProjects/Stephan/Model_data/Paths_15/Training_validating/Paired/input_y.npy'

	# Converting paths to tensors 
	convert_tensor(pathx, pathy)


if __name__ == '__main__':
	main()