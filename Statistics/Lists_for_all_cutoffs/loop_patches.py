# Looping through all files in current dir to perform pre-processing steps

# Modules
import sys
import os 
import numpy as np 

# Files 
from load import *
from patch_criteria import * 

def read(directory, tmp_patches, dim):

    # Amount of pixels in grayscale image
    amount_of_pixels = dim * dim 

    # Go through each plate for each cutoff value 
    for cutoff in range(0, 105, 5):

         # Calculate minimal amount of pixels given cutoff and dim 256
        min_pixels = amount_of_pixels * (cutoff / 100)
        min_pixels = int(min_pixels)

        # Looping through each plate in dir
        for plate_number in os.listdir(directory):

            # Joining the path 
            plate_dir = os.path.join(directory, plate_number)

            # Looping through each fragment belonging to a plate 
            for fragment in os.listdir(plate_dir):

                # Creating the file path to a fragment dir 
                fragment_dir = os.path.join(plate_dir, fragment)

                # Tracking the amount of patches that are according criteria
                track_cutoff = 0

                # Looping through each patch from a fragment 
                for patch in os.listdir(fragment_dir):

                    # Creating the file path to a patch
                    patch_path = os.path.join(fragment_dir, patch)

                    # Load the patch as grayscale
                    gray_patch = load(patch_path, 0)

                    # Checking if the patch meats the cutoff 
                    track_cutoff = track_cutoff + check_patch(gray_patch, min_pixels)

                # If more than 1 patch extrected 
                if track_cutoff > 1:
                    # List of patches per fragment [2, 5, 7, 0, ..] that are according set criteria 
                    # Through len of the arr one can get the amount of fragments
                    tmp_patches.append(track_cutoff)

        # Saving the np array for that criteria 
        np.save("/home/s3690970/Desktop/Bachelor_Project/DSS/Statistics/Lists_for_all_cutoffs/Lists/cnt_patch_" + str(cutoff) + ".npy", tmp_patches)

        # Clearing the list after each run with a criteria 
        tmp_patches.clear()

