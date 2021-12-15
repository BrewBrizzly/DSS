# Splitting array

# Required modules
import numpy as np 
import os 
from sklearn.model_selection import train_test_split

def split_data(path, percentage_training, percentage_testing):

	for arr_name in os.listdir(path):

		# Creating the path to array
		arr_path = os.path.join(path, arr_name)

		# Load the array
		arr = np.load(arr_path, allow_pickle = True)

		# If array not empty
		if arr.any():

			# Confirmation
			print(arr_name)

			# List to store all training/validation
			Training = []

			# List to store all Testing
			Testing = []

			# Looping through all bins to 
			# take % of each 
			Training, Testing = loop_bins(arr, Training, Testing, percentage_training, percentage_testing)

			# Name for dir 
			name = arr_name.split('.npy')
			name = name[0]

			# Checking if dir exists for saving
			if os.path.isdir('/projects/mdhali/BscProjects/Stephan/Model_data/' + name):

				# Saving the training and testing sets
				np.save('/projects/mdhali/BscProjects/Stephan/Model_data/' + name + '/Training_validating /Training-Validation.npy', Training, allow_pickle = True)
				np.save('/projects/mdhali/BscProjects/Stephan/Model_data/' + name + '/Testing/Testing.npy', Testing, allow_pickle = True)
			
			# Create the dirs and save
			else:

				os.makedirs('/projects/mdhali/BscProjects/Stephan/Model_data/' + name + '/Training_validating /')
				np.save('/projects/mdhali/BscProjects/Stephan/Model_data/' + name + '/Training_validating /Training-Validation.npy', Training, allow_pickle = True)

				os.makedirs('/projects/mdhali/BscProjects/Stephan/Model_data/' + name + '/Testing/')
				np.save('/projects/mdhali/BscProjects/Stephan/Model_data/' + name + '/Testing/Testing.npy', Testing, allow_pickle = True)



def loop_bins(arr, Training, Testing, percentage_training, percentage_testing):

	# Loop in order of bins
	# Getting the array belonging to a bin 
	# bin_arr_i[fi[],fn[]]
	for bin_arr in  arr:

		# Confirmation
		print("Bin: ", len(bin_arr[0]))

		# If there are more than 1 fragments in bin
		if len(bin_arr) > 1:

			# Splitting the fragments in the bin array into
			# percentage trainig/val and testing
			tmp_training, tmp_testing = train_test_split(bin_arr, train_size =  percentage_training, test_size = percentage_testing, random_state = 24)

			# Test
			print("Len bin: ", len(bin_arr))
			print("Len x is ", len(tmp_training))
			print("Len y is ", len(tmp_testing))

			# Appending to training and testing sets in a list to preserve bin structure 
			Training.append(tmp_training)
			Testing.append(tmp_testing)

	return Training, Testing

