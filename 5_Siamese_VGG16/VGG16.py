# creating a sister for siamese network 

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten

def build_VGG16_network():
	# initializing the input layer
	inputs = Input(name = 'input', shape = (256,256,3))

	# define the first block of CONV => CONV => POOL layers
	x = Conv2D(name = 'block1_conv1', filters = 64, kernel_size = (3,3), padding = "same", activation = "relu")(inputs)
	x = Conv2D(name = 'block1_conv2', filters = 64, kernel_size = (3,3), padding = "same", activation = "relu")(x)
	x = MaxPooling2D(name = 'block1_pool', pool_size = (2,2), strides = (2,2))(x)

	# second block of CONV => CONV => POOL layers
	x = Conv2D(name = 'block2_conv1', filters = 128, kernel_size = (3,3), padding = "same", activation = "relu")(x)
	x = Conv2D(name = 'block2_conv2', filters = 128, kernel_size = (3,3), padding = "same", activation = "relu")(x)
	x = MaxPooling2D(name = 'block2_pool', pool_size = (2,2), strides = (2,2))(x)

	# third block of CONV => CONV => CONV => POOL layers
	x = Conv2D(name = 'block3_conv1', filters = 256, kernel_size = (3,3), padding = "same", activation = "relu")(x)
	x = Conv2D(name = 'block3_conv2', filters = 256, kernel_size = (3,3), padding = "same", activation = "relu")(x)
	x = Conv2D(name = 'block3_conv3', filters = 256, kernel_size = (3,3), padding = "same", activation = "relu")(x)
	x = MaxPooling2D(name = 'block3_pool', pool_size = (2,2), strides = (2,2))(x)

	# fourth block of CONV => CONV => CONV => POOL layers
	x = Conv2D(name = 'block4_conv1', filters = 512, kernel_size = (3,3), padding = "same", activation = "relu")(x)
	x = Conv2D(name = 'block4_conv2', filters = 512, kernel_size = (3,3), padding = "same", activation = "relu")(x)
	x = Conv2D(name = 'block4_conv3', filters = 512, kernel_size = (3,3), padding = "same", activation = "relu")(x)
	x = MaxPooling2D(name = 'block4_pool', pool_size = (2,2), strides = (2,2))(x)

	# fifth block of CONV => CONV => CONV => POOL layers
	x = Conv2D(name = 'block5_conv1', filters = 512, kernel_size = (3,3), padding = "same", activation = "relu")(x)
	x = Conv2D(name = 'block5_conv2', filters = 512, kernel_size = (3,3), padding = "same", activation = "relu")(x)
	x = Conv2D(name = 'block5_conv3', filters = 512, kernel_size = (3,3), padding = "same", activation = "relu")(x)
	x = MaxPooling2D(name = 'block5_pool', pool_size = (2,2), strides = (2,2))(x)

	# embedding/flattening layer, reducing conv blocks to 1D vector for Eucl. distance 
	outputs = Flatten()(x)

	# build the model
	model = Model(inputs = inputs, outputs = outputs, name = 'VGG16')

	return model 






