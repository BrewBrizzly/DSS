# Required modules
import numpy as np
import shutil


# Loading and returning the numpy arrays
def load_arr(arr1_path, arr2_path, arr_path):

	return np.load(arr1_path, allow_pickle = True), np.load(arr2_path, allow_pickle = True), np.load(arr_path, allow_pickle = True)


# Creating the dir structure
# Storing the RGB images in the structure 
def create_dir(arr1_path, arr2_path, arr_path):

	arr1, arr2, labels = load_arr(arr1_path, arr2_path, arr_path)

	# Cnt positive pairs
	cnt_p = 0

	# Cnt negative pairs
	cnt_n = 0

	# Looping through the paths and the label 
	for path1, path2, label in zip(arr1, arr2, labels):

		# Verify
		print(label)

		# If pair is positive
		if int(label):

			try:
				shutil.copy(path1, '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15/Traing-Validating/Positive/A/' + str(cnt_p) + '.jpg')
				shutil.copy(path2, '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15/Traing-Validating/Positive/B/' + str(cnt_p) + '.jpg')

				# Increase cnt
				cnt_p += 1

				print("Positive pair was copied")

			except PermissionError:

				print('Permission error')
			
			except:

				print('error')

		# If pair is negative
		else:

			try: 
				shutil.copy(path1, '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15/Traing-Validating/Negative/A/' + str(cnt_n) + '.jpg')
				shutil.copy(path2, '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15/Traing-Validating/Negative/B/' + str(cnt_n) + '.jpg')

				# Incease cnt
				cnt_n += 1 

				print("Negative pair was copied")
			
			except PermissionError:

				print('Permission error')
			
			except:

				print('error')



