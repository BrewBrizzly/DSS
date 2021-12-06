# Building a Siamese model 

from VGG16 import *
from utils import * 
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

	# Building the two sisters layers by connecting the input layers and the VGG16
	sister1 = VGG16(input1)
	sister2 = VGG16(input2)

	# Connecting the Sister layers to lambda euclidian distance layer 
	distance = Lambda(euclidean_distance)([sister1, sister2])

	# Creating the final dense layers 
	x = Dense(512, activation="relu", name = 'block6_dense1')(distance)
	x = Dense(512, activation="relu", name = 'block6_dense2')(x)
	outputs = Dense(1, activation="sigmoid", name = 'block6_dense3')(x)

	# building the complete model 
	model = Model(inputs=[CNNTop, CNNBottom], outputs=outputs)	

	print("test")

	# Summary of the complete model 
	model.Summary()

print("Running")
build_VGG16_network((256, 256, 3))
print("Finished")