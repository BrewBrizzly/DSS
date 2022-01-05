# Extracting the patches from the padded fragment

# Modules
import numpy as np 
import cv2
import os 
from skimage.util import view_as_blocks
from unixConv import convert 

def patches(fragment, directory, dir_name_patches, dim):

    # Extracting the patches from the fragment 
    patches = view_as_blocks(fragment, (dim, dim, 3))

    # Saving each patch by going through the collumns and rows of patches
    for col in patches:
        for index, row in enumerate(col):
                        
            # Reducing dimensionality 
            patch = row[0]

            patch_number = convert(index)

            # If patch does not contain only mask, then save
            if np.any(patch):

                # Create a directory for the patches if it does not exist yet 
                if os.path.isdir(directory):
                    cv2.imwrite(directory + dir_name_patches + '-Patch_' +  patch_number + '.jpg', patch)
                else: 
                    os.makedirs(directory)
                    cv2.imwrite(directory + dir_name_patches + '-Patch_' +  patch_number + '.jpg', patch)
