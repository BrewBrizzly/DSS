# Script for extracting patches 

# Required lib

import os 
import cv2
import numpy as np 

# Loops through all patches and passes them to det_pass
def extract_patches(path_to_patches, threshold):

    # Creating a tmp list that keeps track of all the 
    # Fragments/patches belonging to a bin 
    paths_list = []

    # Looping through all the platenumbers 
    for platenumber in os.listdir(path_to_patches):

        # Creating the path to a plate 
        path_platenumber = os.path.join(path_to_patches, platenumber)

        print(path_platenumber)

        # Looping through all the fragments from a plate 
        for fragment in os.listdir(path_platenumber):

            # Creating the path to a fragment 
            path_fragment = os.path.join(path_platenumber, fragment)

            print(path_fragment)

            # Determines, for each fragment, which patches pass the requirement
            # Returns a list of lists containing the paths to the suited patches
            paths_list = det_pass(path_fragment, threshold, paths_list)

    # Creating and saving desired structure 
    create_bins_structure(paths_list)


# Extends a list with a list of paths to patches of a fragment, where a list is equal to a fragment
def det_pass(path_fragment, threshold, paths_list):

    # Temporary list to save all the paths of
    # patches that pass the requirement
    tmp_patch_list = [] 

    # Looping through all the patches of a fragment
    for patch in os.listdir(path_fragment):

        # Create the path to the patch 
        path_patch = os.path.join(path_fragment, patch)

        print(path_patch)

        # Load the patch via cv2 as gray
        patch_img = cv2.imread(path_patch, 0)

        # Determining if image passes threshold
        if cv2.countNonZero(patch_img) >= threshold:

            print("Patch passed")

            # Adding the patch path to tmp_list
            tmp_patch_list.append(path_patch)

    # If there is more than 1 patch extracted 
    if len(tmp_patch_list) > 1: 

        print("list found")

        # Add the paths as a list to the overall structure
        paths_list.append(tmp_patch_list)

    return paths_list


# Extending all the lists of equal len to one list 
# [[paths_belonging_to_same_bin],[...]]
# [[bin_number], [bin_number]]
# Saving that list
def create_bins_structure(paths_list):

    # List to store all the bins values 
    bin_values = []

    # List to store all paths per bin
    binned_list = []

    # Looping through all the lists to determine the bins
    for instance in paths_list:
        bin_number = len(instance)
        if bin_number not in bin_values:
            bin_values.append(len(instance))

    # Sort the bin list increasingly 
    # So that the eventual list is also sorted
    bin_values.sort()

    # looping through all the bin values [2,3,4,...]
    for bin_value in bin_values:

        # Creating a temp list to store all the lists belonging to that bin
        tmp_list = []

        # Going through the complete list to create the appropriate bins
        # as is tmp contains all the paths belonging to a bin
        for instance in paths_list:

            # If the len of a list is equal to a bin value 
            if len(instance) == bin_value:
                tmp_list.extend(instance)

                # Removing the instance from the list
                paths_list.remove(instance)

        # Bin and all its values added to list 
        binned_list.append(tmp_list)

        print("bin created")

    # Save the structers
    save_list('data_set_15.npy', binned_list)
    save_list('bin_set_15.npy', bin_values)

    quick_check(binned_list, bin_values)



# Check if the list are correctly made
def quick_check(binned_list, bin_values):
    print("The len of the data_set is: ", len(binned_list))
    print("The len of the data_set should be equal to that of the bins: ", len(bin_values))
    print("The following bins are included: ", bin_values)

    # Tmp count for totall amount of patches
    tmp_cnt = 0

    for ls, bin_value in zip(binned_list, bin_values):
        print("Bin ", bin_value, " contains ", len(ls), " paths to patches.")
        tmp_cnt += len(ls)
    
    print("Total amount of patches: ", tmp_cnt)

# Saving the list as a numpy struct 
def save_list(name, ls):
    np.save(name, ls)

















