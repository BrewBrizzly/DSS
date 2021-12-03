import numpy as np 


# Creates a struct of all positive and negative
# pairs and their labels
def create_pairs(path, cutoff):

	# Loading the numpy arr containg the lists
	# of bins 
	arr = np.load(path)

	# lists for storing pairs and labels
	# [[pair], [pair], ..]
	# [label, label, label, ..]
	bin_pairs = [] 
	bin_labels_pt = []
	bin_labels_fg = []

	# Looping to each list from a bin 
	for ls in arr:

		# Passing a list of a bin
		bin_pairs, bin_labels_pt, bin_labels_fg = pair(ls, bin_pairs, bin_labels_pt, bin_label_fg)

	# Saving the lists as a np arrays
	np.save('data_pairs_' + cutoff, bin_pairs)
	np.save('data_labels_patch_level_' + cutoff, bin_labels_pt)
	np.save('data_labels_fragment_level_' + cutoff, bin_labels_fg)



# Creates a list of pairs for a bin and the label
def pair(ls, bin_pairs, bin_labels_pt, bin_labels_fg):

	# Stopping criteria 
	end = len(ls)

	# Looping through all paths
	for i in range(len(ls)):

		# Compare index 
		j = i + 1

		# Grabbing all the comparison paths 
		while(j != end):

			# Creating a pair 
			bin_pairs.append([ls[i], ls[j]])

			# Creating the appropriate label for patch level
			bin_labels_pt.append(det_label_pt(ls[i], ls[j]))

			# Creating the appropriate label for fragment level 
			bin_labels_fg.append(det_label_fg(ls[i], ls[j]))

	return 	bin_pairs, bin_labels_pt, bin_labels_fg


# Determining the appropriate label for a pair of patches on patch level
def det_label_pt(base, compare):

	# Determining the name of the patch
	base_name = base.rsplit('/', 1)
	base_name = base_name[1]
	compare_name = compare.rsplit('/', 1)
	compare_name = compare_name[1]

	# Getting the fragment name out 
	base_fragment = base_name.rsplit('-', 1)
	base_fragment = base_fragment[0]
	compare_fragment = compare_name.rsplit('_', 1)
	compare_fragment = compare_fragment[0]

	# If the patches are from the same fragment 
	if base_fragment == compare_fragment:
		return 1
	# If it is not from the same fragment 
	else: 
		return 0 

# Determining the appropriate label for a pair of patches on fragment level 








