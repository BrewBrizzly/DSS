# Required modules
import numpy as np
import shutil


# Loading and returning the numpy arrays
def load_arr(arr1_path, arr2_path):

	return np.load(arr1_path, allow_pickle = True), np.load(arr2_path, allow_pickle = True)

# Storing the RGB images in the structure 
def create_dir(arr1_path, arr2_path):

	arr1, arr2 = load_arr(arr1_path, arr2_path)

	# Cnt the images
	cnt = 0

	# Looping through the first arr
	for path1, path2 in zip(arr1, arr2):

		try:
			shutil.copy(path1, '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15/Traing-Validating/A/' + str(cnt) + '.jpg')
			shutil.copy(path2, '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15/Traing-Validating/B/' + str(cnt) + '.jpg')

			# Increase cnt
			cnt += 1

		except PermissionError:

			print('Permission error')
		
		except:

			print('error')