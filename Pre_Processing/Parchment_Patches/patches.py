# Extracting the patches from the padded fragment

# Modules
import numpy as np 
import cv2
import os 
from skimage.util import view_as_blocks

def patches(fragment, directory, patch_number, n):

	# Extracting the patches from the fragment 
	patches = view_as_blocks(fragment, (256, 256, 3))

	# Saving each patch by going through the collumns and rows of patches
	for col in patches:
		for row in col:
                        
                        # Reducing dimensionality 
                        patch = row[0]

                        # If patch does not contain only mask, then save
                        if np.any(patch):
                                cv2.imwrite(directory + 'Test_Patches/patch_' +  str(patch_number) + '.jpg', patch)
                                patch_number += 1
                        
	return patch_number
