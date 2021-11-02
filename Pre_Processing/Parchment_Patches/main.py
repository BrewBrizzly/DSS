# Extracting 255 by 255 patches from a fragment

# modules
import cv2
import os

# files 

from arg import *
from load import *

def main():

	# Reading the paths to fragment and mask 
	fragment_path = read()

	# Loading the fragment and mask as cv2 struct with flag 1 color and flag 0 gray-scale
	fragment = load(fragment_path, 1)

if __name__ == '__main__':
	main()