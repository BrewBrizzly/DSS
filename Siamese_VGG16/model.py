# Building a Siamese model 

from VGG16 import *
from utils import * 
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Lambda
from tensorflow.keras.datasets import mnist

# Function that connects two CNNS via a ECL layer
# which is connected to a block of dense layers 
def build_Siamese_network(inputShape = 256):

	# Configuring the inputshape of the model 
	imgTop = Input(shape = inputShape)
	imgBottom = Input(shape = inputShape)

	# Functions returns a VGG16 model
	CNNTop = build_VGG16_network(imgTop)
	CNNBottom = build_VGG16_network(imgBottom) 

	# Connecting the Sister networks to lambda euclidian distance layer 
	distance = Lambda(euclidean_distance)([CNNTop, CNNBottom])

	# Creating the final dense layers 
	x = Dense(512, activation="relu", name = 'block6_dense1')(distance)
	x = Dense(512, activation="relu", name = 'block6_dense2')(x)
	outputs = Dense(1, activation="sigmoid", name = 'block6_dense3')(x)

	# building the complete model 
	model = Model(inputs=[CNNTop, CNNBottom], outputs=outputs)	

	# Summary of the complete model 
	model.Summary()

build_VGG16_network()