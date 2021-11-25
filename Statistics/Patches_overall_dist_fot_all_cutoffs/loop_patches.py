# Looping through all files in current dir to perform pre-processing steps

# Modules
import sys
import os 
import numpy as np 

# Files 
from load import *
from patch_criteria import * 

def read(directory, tmp_patches, tmp_fragments, tmp_cutoff, dim):

	# Amount of pixels in grayscale image
	amount_of_pixels = dim * dim 

    # Go through each plate for each cutoff value 
    for cutoff in range(0, 105, 5):

         # Calculate minimal amount of pixels given cutoff and dim 256
        min_pixels = amount_of_pixels * (cutoff / 100)
        min_pixels = int(min_pixels)

        # Initializing the amount of patches for each run 
        amount_of_patches = 0
        amount_of_fragments = 0

        # Looping through each plate in dir
        for plate_number in os.listdir(directory):

            # Joining the path 
            plate_dir = os.path.join(directory, plate_number)

            # If plate_dir is a dir to a plate 
            if os.path.isdir(plate_dir):

                # Looping through each fragment belonging to a plate 
                for fragment in os.listdir(plate_dir):

                        # Creating the file path to a fragment dir 
                        fragment_dir = os.path.join(plate_dir, fragment)

						# If fragment_dir is a dir to a fragment 
            			if os.path.isdir(fragment_dir):

            				# Tracking the amount of patches that are according criteria
            				track_cutoff = 0

            				# Looping through each patch from a fragment 
            				for patch in os.listdir(fragment_dir):

            					# Creating the file path to a patch
                        		patch_path = os.path.join(fragment_dir, patch)

                        		# If path leads to a patch file 
                        		if os.path.isfile(patch_path):

                        			# Load the patch as grayscale
                        			gray_patch = load(patch_path, 0)

               						# Checking if the patch meats the cutoff 
                        			track_cutoff = track_cutoff + check_patch(gray_patch, min_pixels)

                			# Checks if fragment contains at least two patches 
                			if track_cutoff > 1:
	                        	amount_of_patches = amount_of_patches + track_cutoff
	                        	amount_of_fragments += 1  
        
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

