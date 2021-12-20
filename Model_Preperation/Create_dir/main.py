# Creatign a dir structure for positive
# and negative pairs and copying the files to those
# dirs.
# So there is a Postive dir containing a Dir A of the pair
# and a dir B of the pair, and there is a negative dir 
# containing a Dir A of the pair and a Dir B of the pair. 


def main():

	# The path to the lists containing the pairs
	# structure and the paths
	ls1_path = ''
	ls2_path = ''
	lbl_path = ''

	# Creating the dir structure and storing the RGB images
	create_dir(arr1_path, arr2_path, lbl_path)


if __name__ == '__main__':
	main()