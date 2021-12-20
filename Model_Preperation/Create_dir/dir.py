# Required modules
import numpy as np
import os 
import shutil


# Loading and returning the numpy arrays
def load_arr(arr1_path, arr2_path, load_arr)

	return np.load(arr1_path, allow_pickle = True), np.load(arr2_path, allow_pickle = True), np.load(load_arr, allow_pickle = True)


# Creating the dir structure
# Storing the RGB images in the structure 
def create_dir(arr1_path, arr2_path, load_arr):

	arr1, arr2, labels = load_arr(arr1_path, arr2_path, load_arr)

	# Creating the dir structure for positive 
	os.mkdirs('')
	os.mkdirs('')

	# Creating the dir structure for negative
	os.mkdirs('')
	os.mkdirs('')

	# Cnt positive pairs
	cnt_p = 0

	# Cnt negative pairs
	cnt_n = 0

	# Looping through the paths and the label 
	for path1, path2, label in zip(arr1, arr2, labels):

		# If pair is positive
		if label:
			shutil.copy(path1, 'dest/A/' + str(cnt_p) + '.png')
			shutil.copy(path2, 'dest/B/' + str(cnt_p) + '.png')

		# If pair is negative
		else:
			shutil.copy(path1, 'dest/A/' + str(cnt_n) + '.png')
			shutil.copy(path2, 'dest/B/' + str(cnt_n) + '.png')



