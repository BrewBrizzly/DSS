# Looping through all files in current dir to perform pre-processing steps

# Modules
import sys
import os 

# Files 
from load import *
from padding import *
from patches import * 

def read(directory):

	# Keeping track of all patches created 
	patch_number = 0 

	# Looping through each file in a directory 
	for filename in os.listdir(directory):

		# If file is jpg
		if filename.endswith('.jpg'):

			# loading the fragment and mask as cv2 struct with flag 1 color and flag 0 gray-scale
			fragment = load(directory + filename, 1)

			# Padding the fragment to fit n by n patch dimension 
			fragment = padding(fragment, 256)

			# Extracting and saving n by n patches from the fragment 
			patch_number = patches(fragment, directory, patch_number, 256)

