# Looping through all files in current dir to perform pre-processing steps

# Modules
import sys
import os 
import numpy as np 

# Files 
from load import *
from padding import *
from patches import * 

def read(directory, tmp_patches, tmp_fragments, tmp_cutoff):

    # Go through each plate for each cutoff value 
    for cutoff in range(5, 100, 5):

        # Calculate minimal amount of pixels given cutoff and dim 256
        min_pixels = cutoff * 65536 

        # Initializing the amount of patches for each run 
        amount_of_patches = 0
        amount_of_fragments = 0

        # Looping through each plate in dir
        for plate_number in os.listdir(directory):

            # Joining the path 
            plate_number = os.path.join(directory, plate_number)

            # If d is a dir to a plate 
            if os.path.isdir(plate_number):

                # Looping to each fragment belonging to a plate 
                for filename in os.listdir(plate_number):

                    # If file is jpg
                    if filename.endswith('.jpg'):

                        # Creating the file path 
                        file_path = os.path.join(plate_number, filename)

                        # loading the fragment and mask as cv2 struct with flag 1 color and flag 0 gray-scale
                        fragment = load(file_path, 1)

                        # Padding the fragment to fit n by n patch dimension 
                        fragment = padding(fragment, 256)

                        # Counting the amount of patches extracted from a fragment at a certain cutoff 
                        amount_of_patches, amount_of_fragments = count_patches(fragment, 256, min_pixels, amount_of_patches, amount_of_fragments)
        
        # Adding the count and cutoff to the array 
        tmp_patches.append(amount_of_patches)
        tmp_fragments.append(amount_of_fragments)
        tmp_cutoff.append(cutoff)

    # Stacking the two lists so to create a histogram 
    stacked_patches = np.stack((tmp_patches, tmp_cutoff))
    stacked_fragments = np.stack((tmp_fragments, tmp_cutoff))

    # Saving the np array
    np.save("/home/p301438/Python/stat/count_patches.npy", stacked_patches)
    np.save("/home/p301438/Python/stat/count_fragments.npy", stacked_fragments)

