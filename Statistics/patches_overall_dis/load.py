# Given a path teruns the image as a cv2 struct

# Modules
import cv2

def load(path, flag):
	return cv2.imread(path, flag)