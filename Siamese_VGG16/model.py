# Building the Siamese model 

from VGG16 import *
from utils import * 
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Lambda
from tensorflow.keras.datasets import mnist

def build_Siamese_network():
	# configure the Sister networks
	imgA = Input(shape= inputShape)
	imgB = Input(shape= inputShape)
	featureExtractor = build_VGG16_network(inputShape)
	featsA = featureExtractor(imgA)
	featsB = featureExtractor(imgB) 

	# Connecting the Sister networks to lambda euclidian distance layer 
	distance = Lambda(euclidean_distance)([featsA, featsB])

	# Creating the final dense layers 
	x = Dense(512, activation="relu")(distance)
	x = Dense(512, activation="relu")(x)
	outputs = Dense(1, activation="sigmoid")(x)

	# building the complete model 
	model = Model(inputs=[imgA, imgB], outputs=outputs)	

	# Summary of the complete model 
	model.Summary()