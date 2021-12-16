# Converting to tensors

# Required modules
import tensorflow as tf 
import numpy as np 
import cv2

def convert_tensor(path_arr1, path_arr2):

	# Loading the x and y array
	arr_x = np.load(path_arr1, allow_pickle = True)
	arr_y = np.load(path_arr2, allow_pickle = True)

	# Creating empty lists to store the tensors in 
	tens_x = []
	tens_y = []

	# Count to keep track of arrays created
	cnt = 0

	# get the paths of x and y
	for i in range(len(arr_x)):

		print(i)

		# reading, converting and appending the rgb image of x 
		img_bgr_x = cv2.imread(arr_x[i])
		img_rgb_x = cv2.cvtColor(img_bgr_x, cv2.COLOR_BGR2RGB)
		img_tensor_x = tf.convert_to_tensor(img_rgb_x, dtype = tf.float32)

		tens_x.append(img_tensor_x)

		# reading, converting and appending the rgb image of y
		img_bgr_y = cv2.imread(arr_y[i])
		img_rgb_y = cv2.cvtColor(img_bgr_y, cv2.COLOR_BGR2RGB)
		img_tensor_y = tf.convert_to_tensor(img_rgb_y, dtype = tf.float32)

		tens_y.append(img_tensor_y)

		# Preserving system memory
		if ((i % 2500 == 0) and (i > 0)) or i == (len(arr_x) - 1):

			# Confirmation
			print("Len x: ", len(arr_x))
			print("Len tensors x: ", len(tens_x))

			print("Len y: ", len(arr_y))
			print("Len tensors y: ", len(tens_y))

			# Saving the arrays of tensors
			np.save('/projects/mdhali/BscProjects/Stephan/Model_data/Paths_15/Training_validating/Paired_Converted/tensors_x_' + str(cnt) + '.npy', tens_x, allow_pickle = True)
			np.save('/projects/mdhali/BscProjects/Stephan/Model_data/Paths_15/Training_validating/Paired_Converted/tensors_y_' + str(cnt) + '.npy', tens_y, allow_pickle = True)

			# Clearing the tensor arrays
			tens_x.clear()
			tens_y.clear()

			# Increasing cnt 
			cnt += 1
	





