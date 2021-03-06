# Creating a bin structure in the arrays

# Requiered libraries
import numpy as np 
import os

# Looping through all the arrays
def loop_arrays(path):

	# Looping through all the arrays in the dir 
	for arr_file in os.listdir(path):

		# Checking if the file is a numpy array 
		if arr_file.endswith('.npy'):

			# Creating the path to an array
			arr_path = os.path.join(path, arr_file)

			# Loading the array
			arr = np.load(arr_path, allow_pickle = True)

			# Creating a sorted bins list for an array
			bins_ls = create_bins_ls(arr)

			# Confirmation
			print("Bins: ", bins_ls)

			# Creating the bin structure in the array
			create_bins_structure(arr, bins_ls, arr_file)


# Create a list containing all the bins 
def create_bins_ls(arr):

	# Creating a list containing an oredered bins of array
	bins_ls = []

	# Looping through all instances to get the bin values
	for instance in arr:

		# If bin value is not in the list 
		if len(instance) not in bins_ls:

			bins_ls.append(len(instance))

	# Order the bin list 
	bins_ls.sort()

	# Returning the sorted list 
	return bins_ls

# Creating the bin structure in an array
# bin_strc_i[tmp_bin_i[fragment_i[]]]
def create_bins_structure(arr, bins, name):

	# List for bin structure
	bin_strc = []

	# Looping through all the bin values in order
	for i in range(len(bins)):

		# Storing all the fragments belonging to a bin
		tmp_bin = [] 

		# Looping through paths in array 
		for instance in arr:

			# If a instane of paths belongs to a bin 
			if len(instance) == bins[i]:

				tmp_bin.append(instance)

		bin_strc.append(tmp_bin)

	# Storing the bin_struct 
	np.save('/projects/mdhali/BscProjects/Stephan/Sorted_paths/Arrays/' + name, bin_strc, allow_pickle = True)

	# Confirmation
	print("Saved: " + name)














