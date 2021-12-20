# Converting to tensors

# Required modules
import tensorflow as tf 
import numpy as np 
import cv2
import os 

def convert_tensor(path):

	# Creating the desired dir structure positive
	os.mkdirs('dir/Positive/A/')
	os.mkdirs('dir/Positive/B/')

	# Creating the desired negative dir structure 
	os.mkdirs('dir/Negative/A/')
	os.mkdirs('dir/Negative/B/')


	# Looping through the positive and negative dir
	for label_dir in os.listdir(path):

		label_path = os.path.join(path, label_dir)

		# If positive dir 
		if label_dir == 'Positive':

			# First looping through the positive RGBS
			for directory_name in os.listdir(path_p):

				directory_path = os.path.join(path_p, directory_name)

				# If A
				if directory_name == 'A':

					# Looping through all images in A and B
					for image_name in directory_path:

						# Image path
						image_path = os.path.join(directory_path, image_name)

						# reading, converting and appending the rgb image of x 
						img_bgr_x = cv2.imread(image_path)
						img_rgb_x = cv2.cvtColor(img_bgr_x, cv2.COLOR_BGR2RGB)
						img_tensor_x = tf.convert_to_tensor(img_rgb_x, dtype = tf.float32)

						# Saving
						np.save('dir/Positive/A/', img_tensor_x)

				# If B
				else:

					# Looping through all images in A and B
					for image_name in directory_path:

						# Image path
						image_path = os.path.join(directory_path, image_name)

						# reading, converting and appending the rgb image of x 
						img_bgr_x = cv2.imread(image_path)
						img_rgb_x = cv2.cvtColor(img_bgr_x, cv2.COLOR_BGR2RGB)
						img_tensor_x = tf.convert_to_tensor(img_rgb_x, dtype = tf.float32)

						# Saving
						np.save('dir/Positive/B/', img_tensor_x)


		# If negative dir 
		if label_dir == 'Negative':

			# First looping through the positive RGBS
			for directory_name in os.listdir(path_p):

				directory_path = os.path.join(path_p, directory_name)

				# If A
				if directory_name == 'A':

					# Looping through all images in A and B
					for image_name in directory_path:

						# Image path
						image_path = os.path.join(directory_path, image_name)

						# reading, converting and appending the rgb image of x 
						img_bgr_x = cv2.imread(image_path)
						img_rgb_x = cv2.cvtColor(img_bgr_x, cv2.COLOR_BGR2RGB)
						img_tensor_x = tf.convert_to_tensor(img_rgb_x, dtype = tf.float32)

						# Saving
						np.save('dir/Negative/A/', img_tensor_x)


				# If B
				else:

					# Looping through all images in A and B
					for image_name in directory_path:

						# Image path
						image_path = os.path.join(directory_path, image_name)

						# reading, converting and appending the rgb image of x 
						img_bgr_x = cv2.imread(image_path)
						img_rgb_x = cv2.cvtColor(img_bgr_x, cv2.COLOR_BGR2RGB)
						img_tensor_x = tf.convert_to_tensor(img_rgb_x, dtype = tf.float32)

						# Saving
						np.save('dir/Negative/B/', img_tensor_x)


# Why not use tf.keras.utils.image_dataset_from_directory

	





