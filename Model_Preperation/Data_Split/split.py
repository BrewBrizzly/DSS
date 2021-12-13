# Splitting array

# Required modules
import numpy as np 
from sklearn.model_selection import train_test_split

def split_data(path, percentage_training, percentage_testing):

	# Load the array
	arr = np.load(path)

	# List to store all training/validation
	Training = []

	# List to store all Testing
	Testing = []

	# Looping through all bins to 
	# take % of each 
	Training, Testing = loop_bins(Training, Testing, percentage_training, percentage_testing)

	# Saving the training and testing sets
	np.save('Training/Validation.npy', Training)
	np.save('Testing.npy', Testing)


def loop_bins(arr, Training, Testing, percentage_training, percentage_testing):

	# Loop in order of binds
	for i in len(range(arr)):

		# Getting the array belonging to a bin 
		bin_arr = arr[i]

		# Splitting the fragments in the bin array into
		# percentage trainig/val and testing
		tmp_training, tmp_testing = train_test_split(bin_arr, train_size =  percentage_training, test_size = percentage_testing, random_state = 24)

		# Appending to training and testing sets
		Training.append(tmp_training)
		Testing.append(tmp_testing)

	return Training, Testing

