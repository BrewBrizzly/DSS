# Required modules
import numpy as np 
import shutil


# Loading and returning the numpy arrays
def load_arr(arr1_path, arr2_path, label_path):

	return np.load(arr1_path, allow_pickle = True), np.load(arr2_path, allow_pickle = True), np.load(label_path)

# Storing the RGB images in the structure 
def create_dir(arr1_path, arr2_path, label_path):

	arr1, arr2, labels = load_arr(arr1_path, arr2_path, label_path)

	# Cnt the images in alphanumeric order 
	cnt_p = 0
	cnt_n = 0

	# Looping through the first arr
	for path1, path2, label in zip(arr1, arr2, labels):

		# Setting the format 
		exp = 1

		# Building conventional dir 
		if not exp:

			# if positive pair
			if int(label): 

				try:
					shutil.copy(path1, '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15/Training-Validation/A/' + str(cnt_p) + 'P.jpg')
					shutil.copy(path2, '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15/Training-Validation/B/' + str(cnt_p) + 'P.jpg')

					# Increase cnt
					cnt_p += 1

				except PermissionError:

					print('Permission error')
				
				except:

					print('error')
			
			# If negative pair
			else:

				try:
					shutil.copy(path1, '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15/Training-Validation/A/' + str(cnt_n) + 'N.jpg')
					shutil.copy(path2, '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15/Training-Validation/B/' + str(cnt_n) + 'N.jpg')

					# Increase cnt
					cnt_n += 1

				except PermissionError:

					print('Permission error')
				
				except:

					print('error')

		# Building experimental dir strc 
		else: 

			# if positive pair
			if int(label): 

				try:
					shutil.copy(path1, '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15_exp/Training/Positive/A/' + str(cnt_p) + 'P.jpg')
					shutil.copy(path2, '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15_exp/Training/Positive/B/' + str(cnt_p) + 'P.jpg')

					# Increase cnt
					cnt_p += 1

				except PermissionError:

					print('Permission error')
				
				except:

					print('error')
			
			# If negative pair
			else:

				try:
					shutil.copy(path1, '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15_exp/Training/Negative/A/' + str(cnt_n) + 'N.jpg')
					shutil.copy(path2, '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15_exp/Training/Negative/B/' + str(cnt_n) + 'N.jpg')

					# Increase cnt
					cnt_n += 1

				except PermissionError:

					print('Permission error')
				
				except:

					print('error')

