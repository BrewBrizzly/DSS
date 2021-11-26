# Counting non black pixels in patch and checking set criteria 

# Modules
import cv2

def check_patch(patch, min_pixels):

	# Checking the amount of pixels that are not black
    if cv2.countNonZero(patch) >= min_pixels:
    	return 1
    else:
    	return 0
