# Extracting the patches from the padded fragment

# Modules
import numpy as np 
import cv2
import os 
# from skimage.util import view_as_blocks

def count_patches(fragment, dim, min_pixels, amount_of_patches):

    # Extracting the patches from the fragment 
    patches = view_as_blocks(fragment, (dim, dim, 3))

    # Temporary object to track the amount of patches that meat the cutoff criteria
    tmp_cnt = 0 

    # Saving each patch by going through the collumns and rows of patches
    for col in patches:
        for index, row in enumerate(col):
                        
            # Reducing dimensionality 
            patch = row[0]

            # Gray patch for counting the fraction of black pixels in patch 
            gray_patch = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)

            # If patch contains atleas cutoff% patch, then add it to the count 
            if cv2.countNonZero(gray_patch) >= min_pixels:
                tmp_cnt += 1

    # If more than 2 patches were found, then add the total  
    if tmp_cnt > 1:
        amount_of_patches += amount_of_patches + tmp_cnt

    return amount_of_patches
