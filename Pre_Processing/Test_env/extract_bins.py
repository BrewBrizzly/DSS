# Creating a bin structure in the lists

# Requiered libraries
import numpy as np 

# Looping through all the arrays
def loop_lists():
	
	# Setting the path
	path = ''

	# Looping through all the arrays in the dir 
	for arr_file in os.listdir(path):

		# Creating the path to an array
		arr_path = os.dir.join(path, arr_file)

		# Loading the array
		arr = np.load(arr_path, allow_pickle = True)

		# Creating a sorted bins list for an array
		bins_ls = create_bins_ls(arr)

		# Creating the bin structure in the array
		create_bins_structure(arr, bins_ls, arr_file)


# Create the bin structure for an array
def create_bins_ls(arr):

	# Creating a list containing an oredered bins of array
	bin_ls = []

	# Looping through all instances to get the bin values
	for instance in arr:

		# If bin value is not in the list 
		if len(instance) not in bin_ls:

			bin_ls.append(instance)

	# Order the bin list 
	bin_ls.sort()


# Creating the bin structure in an array
def create_bins_structure(arr, bins, name)

	# List for bin structure
	bin_strc = []

	# Looping through all the bin values 
	for i in range(len(bins)):

		# Storing a single bin structure 
		tmp_bin = [] 

		# Looping through paths in array 
		for instance in arr:

			# If a instane of paths belongs to a bin 
			if len(instance) == bn[i]:

				tmp_bin.extend(instance)

		bin_strc.append(instance)

	# Storing the bin_struct 
	np.save('Lists_sorted/' + name, bin_strc, allow_pickle = True)














