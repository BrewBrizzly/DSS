# Script for storing images in the desired dir struct 

# Required libraries
from dir_strc import * 


def main():

	# The path to the lists containing the pairs
	# structure and the paths
	arr1_path = '/projects/mdhali/BscProjects/Stephan/Paths/Sorted_Paths_Split_Paired/Cutoff_15/Training_Validating/Paired/input_x.npy'
	arr2_path = '/projects/mdhali/BscProjects/Stephan/Paths/Sorted_Paths_Split_Paired/Cutoff_15/Training_Validating/Paired/input_y.npy'
	label_path = '/projects/mdhali/BscProjects/Stephan/Paths/Sorted_Paths_Split_Paired/Cutoff_15/Training_Validating/Paired/labels.npy'

	# Creating the dir structure and storing the RGB images
	create_dir(arr1_path, arr2_path, label_path)


if __name__ == '__main__':
	main()