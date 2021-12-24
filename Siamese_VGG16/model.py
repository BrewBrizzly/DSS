# Building a Siamese model 

from VGG16 import *
from utils import * 
import numpy as np
import tensorflow as tf
from tensorflow import keras
# from tensorflow.keras.models import Model
# from tensorflow.keras.layers import Dense
# from tensorflow.keras.layers import Input
# from tensorflow.keras.layers import Lambda

# Just disables the warning, doesn't take advantage of AVX/FMA to run faster
# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Function that connects two CNNS via a ECL layer
# which is connected to a block of dense layers 
def build_Siamese_network():

	# Configuring input layers for each sister
	Input_Image_A = Input(name = 'Image_A', shape = (256, 256, 3))
	Input_Image_B = Input(name = 'Image_B', shape = (256, 256, 3))

	# Defining the VGG16
	VGG16 = build_VGG16_network()

	# Connecting each image to VGG16
	VGG16_A = VGG16(Input_Image_A)
	VGG16_B = VGG16(Input_Image_B)

	# Connecting the each layer to lambda euclidian distance layer 
	distance = keras.layers.Lambda(euclidean_distance)([VGG16_A, VGG16_B])

	# Creating the final dense layers 
	x = keras.layers.Dense(512, activation="relu", name = 'block6_dense1')(distance)
	x = keras.layers.Dense(512, activation="relu", name = 'block6_dense2')(x)
	outputs = keras.layers.Dense(1, activation="sigmoid", name = 'block6_dense3')(x)

	# building the complete model 
	model = Model(inputs=[Input_Image_A, Input_Image_B], outputs=outputs, name = 'Siame_Network')	

	return model


# Building the left and right dataset
def build_data(dir_A, dir_B):

	# Load A and B dataset

	train_ds_A = tf.keras.utils.image_dataset_from_directory(directory = dir_A, labels = None, label_mode = None, shuffle = True, seed = 32, batch_size = 16)
	train_ds_B = tf.keras.utils.image_dataset_from_directory(directory = dir_B, labels = None, label_mode = None, shuffle = True, seed = 32, batch_size = 16)

	# Check if the order is still correct 

	A_paths = train_ds_A.file_paths
	B_paths = train_ds_B.file_paths

	print(A_paths[0:2])
	print(B_paths[0:2])

	# Scaling the data 
	normalize_layer = tf.keras.layers.Rescaling(1./255)
	train_ds_A = train_ds_A.map(lambda x: normalize_layer(x))
	train_ds_B = train_ds_B.map(lambda x: normalize_layer(x))

	# Building the labels 
	labels = build_labels(A_paths)

	return train_ds_A, train_ds_B, labels


# Build labels
def build_labels(A_paths):

	# Now create the label list 

	labels = []

	for path in A_paths:

		splitted = path.split('.jpg')
		splitted = splitted[0]
		if(splitted[-1]) == 'P':
			labels.append(1)
		else:
			labels.append(0)
	
	return np.array(labels)



# Builds the data and model to train it 
def train(Dir_A, Dir_B):

	# Settings for GPU, and a check
	phy_dev = tf.config.experimental.list_physical_devices('GPU')
	print("Num gpu: ", len(phy_dev))
	tf.config.experimental.set_memory_growth(phy_dev[0], True)

	# Getting the dataset into Tensorflow format 
	left_ds, right_ds, labels = build_data(Dir_A, Dir_B)

	# Confirmation of total data
	print("Each struct has length: ", len(labels))

	# Building the model with the dimensions of a patch
	model = build_Siamese_network()

	# Summary of the model as confirmation
	model.summary()

	# Compiling the model, default adam learning rate is 0.001
	model.compile(loss = "binary_crossentropy", optimizer = "adam", metrics = ["accuracy"])

	# Training the model, epochs 100 set similar to paper, for test to 10 
	model.fit([left_ds, right_ds], labels) # y = labels, epochs = 10, validation_split = 0.2)

	# Saving the model after training 
	hist = model.save('/projects/mdhali/BscProjects/Stephan/Model/')

	# Printing the history
	print(hist)








