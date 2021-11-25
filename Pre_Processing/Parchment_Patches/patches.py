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

            # Gray patch for counting the fraction of black pixels in patch 
            gray_patch = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)

            # If patch does not contain 5% or more mask, then save 
            if cv2.countNonZero(gray_patch) > 3277:

                patch_number = convert(index)

                # Create a directory for the patches if it does not exist yet 
                if os.path.isdir(directory):
                    cv2.imwrite(directory + dir_name_patches + '-Patch_' +  patch_number + '.jpg', patch)
                else: 
                    os.makedirs(directory)
                    cv2.imwrite(directory + dir_name_patches + '-Patch_' +  patch_number + '.jpg', patch)
