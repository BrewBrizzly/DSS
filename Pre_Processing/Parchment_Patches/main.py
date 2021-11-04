# Extracting 255 by 255 patches from a fragment

# modules
import cv2
import os

# files 
from arg import *
from load import *
from padding import *
from patches import * 

# /Users/stephannijdam/Desktop/DSS/Pre_Processing/Parchment_Patches/test.jpg

def main():

	# Reading the paths to fragment and mask 
	fragment_path = read()

	# loading the fragment and mask as cv2 struct with flag 1 color and flag 0 gray-scale
	fragment = load(fragment_path, 1)

	# Padding the fragment to fit n by n patch dimension 
	fragment = padding(fragment, 256)

	# Extracting and saving n by n patches from the fragment 
	# patches(fragment)

if __name__ == '__main__':
	main()