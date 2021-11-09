# Looping through all files in current dir to perform pre-processing steps

# Modules
import sys
import os 

# Files 
from load import *
from padding import *
from patches import * 

def read(directory):

    # Looping through each plate in dir
    for plate_number in os.listdir(directory):

        # Keeping track of all patches created per fragment
        n = 0 

        # Joining the path 
        d = os.path.join(directory, plate_number)

        # If d is a dir to a plate 
        if os.path.isdir(d):

            # Looping to each fragment belonging to a plate 
            for filename in os.listdir(plate_number):

                # If file is jpg
                if filename.endswith('.jpg'):

                    # Creating the file path 
                    file_path = d + '/' + filename

                    # Creating the dir name for the patches to be stored 
                    dir_name_patches = filename.split('.')
                    dir_name_patches = dir_name_patches[0]

                    # loading the fragment and mask as cv2 struct with flag 1 color and flag 0 gray-scale
                    fragment = load(file_path, 1)

                    # Padding the fragment to fit n by n patch dimension 
                    fragment = padding(fragment, 256)

                    # Extracting and saving n by n patches from the fragment 
                    patch_number = patches(fragment, 'data/p301438/IAApatches_parchment_onlyColor-resized50/' + plate_number + '/' + dir_name_patches + '/', n, 256)

