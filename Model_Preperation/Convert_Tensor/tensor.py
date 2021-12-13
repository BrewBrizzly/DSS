# Converting to tensors

# Required modules
import tensorflow as tf 
import numpy as np 
import cv2


def convert_tensor(path_arr):

	# Loading the array
	arr = np.load(path_arr)

	# List to store the tensors
	tensor_ls = []

	# get the paths 
	for bin_number in arr:

		# tmp ls for bin 
		tmp_bin = []

		for fragment in bin_number:

			# tmp for fragment
			tmp_fragment = [] 

			for path in fragment:

				# reading the rgb image
				img_bgr = cv2.imread(path)
				img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

				# converting to tensor 
				img_tensor = tf.convert_to_tensor(img_rgb, dtype = tf.float32)

				# Append to fragment list
				tmp_fragment.append(img_tensor)

			# Append to bin list 
			tmp_bin.append(tmp_fragment)

		# Append bin to tensor list
		tensor_ls.append(tmp_bin)

	# Saving the converted tensors
	np.save('Tensors.npy', tensor_ls)

