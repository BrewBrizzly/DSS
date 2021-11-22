# Extracting the patches from the padded fragment

# Modules
import numpy as np 
import cv2
import os 
from skimage.util import view_as_blocks
from unixConv import convert 

def patches(fragment, directory, dim):

    # Extracting the patches from the fragment 
    patches = view_as_blocks(fragment, (dim, dim, 3))

    # Saving each patch by going through the collumns and rows of patches
    for col in patches:
        for index, row in enumarte(col):
                        
            # Reducing dimensionality 
            patch = row[0]

            # If patch does not contain only mask, then save !!! Namingconv???? use 001 and remove after D 
            if np.any(patch):
                    cv2.imwrite(directory + '-Patch_' +  convert(index) + '.jpg', patch)
            
    return patch_number
