# Required libs
import numpy as np 
import cv2
import os

# Creates a list that stores the paths for each cutoff
# as in: [ [ [paths_fragment], [paths_fragment], .. ], [paths for fragments cutoff ..]]
def ceate_paths(path):

    # Creating a list containing the min amount of 
    # patches for a given cutoff 
    cutoff_list, min_pixels = det_pixels_and_lists(256)

    # Looping through all the plates in the dir 
    for plate in os.listdir(path):

        plate_path = os.path.join(path, plate)

        # Looping through all the framgnents in the dir 
        for fragment in os.listdir(plate_path):

            fragment_path = os.path.join(plate_path, fragment)

            # Looping through all the patches belonging to a fragment
            cutoff_list = loop_patches(fragment_path, cutoff_list, min_pixels) 

    # Saving the list of paths for each cutoff point
    save_lists(cutoff_list)


# Returns an ordered list of the minimum amount of pixels given a cutoff % 
# as in: [pixels at 0%, pixels at 5%]
def det_pixels_and_lists(dim):

    # Calculating the amount of pixels 
    amount_of_pixels = dim * dim 

    # List to store all minimum amount of pixels 
    pixel_list = []

    # List to store a list for each cutoff
    cutoff_list = []

    # Cutoff percentage from 0 to and including 100
    for cutoff in range(0, 105, 5):

        # Calculate minimal amount of pixels given cutoff and dim 256
        min_pixels = amount_of_pixels * (cutoff / 100)
        min_pixels = int(min_pixels)

        # Appending the minimum amount of pixels to the list 
        pixel_list.append(min_pixels)

        # Appending a list 
        cutoff_list.append([])

    return cutoff_list, pixel_list


# Looping through all the plates belonging to a fragment
# Creating a list as in: pop the list for a cutoff,
# and fill it with the paths for that fragments:
# [[paths_fragment], [paths_fragment]]
def loop_patches(fragment_path, cutoff_list, min_pixels):  

    # Keeping track of all the fragments that are passed
    print(fragment_path)  

    # Go through each plate for each cutoff value 
    # with steps of 5%
    for i in range(0, 21, 1):

        # Setting the min pixels for this run 
        minimum = min_pixels[i]		

        # Getting the list to store the list of paths in 
        paths_list = cutoff_list[i]

        # Temporary list to store the paths in 
        tmp_ls = []

        # Count to keep track of the amount of patches that pass the cutoff 
        count = 0

        # Looping through the plates of a fragment for a given cutoff 
        for patch in os.listdir(fragment_path):

            # The path to the patch
            patch_path = os.path.join(fragment_path, patch)

            # Load the patch as grayscale
            patch_img = cv2.imread(patch_path, 0)

            # Determine if the patch has the appropriate
            # amount of pixels 
            if cv2.countNonZero(patch_img) >= minimum:

                # A patch that matches the criteria 
                count += 1 

                # Store the path in the list
                tmp_ls.append(patch_path)

        # Checking how many patches passed
        if count > 1:

            # Append the paths to the correct list
            paths_list.append(tmp_ls)

    return cutoff_list


# Saving the list for each cutoff 
def save_lists(cutoff_list):

    # Creating a list with the appropriate extentions
    ext = [] 

    for e in range(0, 105, 5):
        ext.append(str(e))

    # Go through each list for each cutoff value 
    # with steps of 5% and save the list
    for i in range(0, 21, 1):

        # Storing the list of paths for a cutoff
        np.save('/home/s3690970/Desktop/Bachelor_Project/DSS/Pre_Processing/Test_env/Lists/Paths_' + ext[i] + '.npy' , cutoff_list[i], allow_pickle = True)



















