# Script for extracting patches 

# Required lib 

import os 
import cv2
import numpy as np 

# Loops through all patches and passes them to det_pass
def extract_patches(path_to_patches, path_to_save, threshold):

	# Creating a tmp list that keeps track of all the 
	# Fragments/patches belonging to a bin 
	data_path = []

	# Looping through all the platenumbers 
	for platenumber in os.path.listdirs(path_to_patches):

		# Creating the path to a plate 
		path_platenumber = os.path.join(path_to_patches, platenumber)

		# Looping through all the fragments from a plate 
		for fragment in os.path.listdirs(path_platenumber):

			# Creating the path to a fragment 
			path_fragment = os.path.join(path_platenumber, path_fragment)

			# Determines, for each fragment, which patches pass the requirement
			# Returns a list to update the bins and its members 
			data_path = det_pass(path_fragment, path_to_save, platenumber, fragment, threshold)

	# Adding all the lists of equal len to same bins 
	create_bins(data_path)


# Determines if a patch should be copied to the data directory
# creates a list of all bins and their patches 
def det_pass(path_fragment, path_to_save, platenumber, fragment, threshold, data_path):

	# Looping through all the patches of a fragment
	for patch in os.path.listdirs(path_fragment):

		# Temporary list to save all the paths of
		# Patches that pass the requirement
		tmp_list = [] 

		# Cnt all patches that pass the requirement 
		cnt_patch = 0

		# Create the path the the patch 
		path_patch = os.path.join(path_fragment, patch)

		# Load the patch via cv2 as gray
		patch_img = cv2.imread(path_patch, 0)

		# Determining if image passes threshold
		if cv2.countNonZero(patch_img) >= threshold:

			# Increase the count
			cnt_patch += 1 

			# Creating the save path 
			save = os.dir.join(path_to_save + platenumber + fragment)

			# Adding the patch path to tmp_list
			tmp_list.append(save + patch)

			# Check if fragment folder already exists
			if os.dir.isdir(save):

				# rsync the patch to the data-set 
				os.system("rsync -avnP " + path_patch + ' ' + save) 

			else: 

				# Creating the directory for saving 
				os.mkdirs(save)
				
				# rsync the patch to the data-set 
				os.system("rsync -avnP " + path_patch + ' ' + save) 

	# If there is more than 1 patch extracted 
	if cnt_patch > 1: 
		data_path.append(tmp_list)

	return data_path

# Creates the bins in a list 
def create_bins(data):

	# List to store all the bins values 
	bins = []

	# Looping through all the lists to determine the bins
	for instance in data:
		bin_number = len(instance)
		if bin_number is not in bins:
			bins.append(len(instance))

	# looping through all the bin values 
	for bin_value in bins:

		# Creating a temp list to store all the lists belonging to that bin
		tmp_list = []

		# Going through the complete list to check create the appropriate bins
		# In the list structure
		for instance in data:

			if len(instance) == bin_value:
				tmp_list.extend(instance)

				# Removing the instance from the list
				data.remove(instance)

		# Bin and all its values added to list 
		data.append(tmp_list)

	# Save the struct 
	np.save('data_set.npy', data)













