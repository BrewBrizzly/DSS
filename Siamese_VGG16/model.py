# Building a Siamese model 

from VGG16 import *
from utils import * 
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Lambda
from tensorflow.keras.datasets import mnist

# Just disables the warning, doesn't take advantage of AVX/FMA to run faster
# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Function that connects two CNNS via a ECL layer
# which is connected to a block of dense layers 
def build_Siamese_network(inputShape):

	# Configuring input layers for each sister
	input1 = Input(shape = inputShape)
	input2 = Input(shape = inputShape)

	# Configuring a VGG16 model based on the input shape 
	VGG16 = build_VGG16_network(inputShape)

	# Building the two sisters layers by combining the input layers and the VGG16
	sister1 = VGG16(input1)
	sister2 = VGG16(input2)

	# Connecting the Sister layers to lambda euclidian distance layer 
	distance = Lambda(euclidean_distance)([sister1, sister2])

	# Creating the final dense layers 
	x = Dense(512, activation="relu", name = 'block6_dense1')(distance)
	x = Dense(512, activation="relu", name = 'block6_dense2')(x)
	outputs = Dense(1, activation="sigmoid", name = 'block6_dense3')(x)

	# building the complete model 
	model = Model(inputs=[sister1, sister2], outputs=outputs)	

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
	
	return labels



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
	model = build_Siamese_network((256, 256, 3))

	# Summary of the model as confirmation
	model.summary()

	# Compiling the model, default adam learning rate is 0.001
	model.compile(loss = "binary_crossentropy", optimizer = "adam", metrics = ["accuracy"])

	# Training the model, epochs 100 set similar to paper, for test to 10 
	model.fit(x = [left_ds, right_ds], y = labels) # y = labels, epochs = 10, validation_split = 0.2)

	# Saving the model after training 
	hist = model.save('/projects/mdhali/BscProjects/Stephan/Model/')

	# Printing the history
	print(hist)








