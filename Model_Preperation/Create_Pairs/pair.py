# Creating and saving positive and 
# negative pairs


# Required modules 
import numpy as np 



# Creating the negative pair
# by going through all even fragments
# and maximizing the distance 
def create_negative(even, x, y, labels):

	# Defining the starting indexes
	i = 0
	j = len(even) - 1

	# Setting current odd length 
	odd_len = len(x)

	# While item i is equal to item j or 
	# length even is equal to length odd
	while((even[i] != even[j]) or (len(even) != odd_len)):

		# Creating the negative pair
		x.append(even[i])
		y.append(even[j])
		labels.append(0)

	return x, y, labels


# Creating the positive pairs
# by going through odd fragments
def create_positive(arr, x, y, labels, even):

# Looping through the bins 
	for bn in arr:

   	# looping through the fragments in a binn
   	for index, fragment in enumerate(bn): 

   		# If even 
   		if (index % 2) == 0:

   			# extending fragment's tensors to even list 
   			even.extend(fragment)

   		# If odd
   		else:

   			# Defining stop loop
   			stop = len(fragment)

   			# Looping through all tensors in fragment
   			for i, tensor in enumerate(fragment):

   				j = i + 1 

   				# Create the pair 
   				while(j < stop):

   					# The pair 
   					x.append(tensor)
   					y.append(fragment[j])
   					labels.append(1)

   	return even, x, y, labels


def create_pairs(path):

	# Load the array 
    arr = np.load(path)

    # list for x and y of pair
    input_x = []
    input_y = []

    # list for the label of pair x y
    labels = []

    # Creating a list for even fragments
    even = []

    # Creating the positive pairs
    even, input_x, input_y, labels = create_positive(arr, input_x, input_y, labels)

    # Creating the negative pairs
    input_x, input_y, labels = create_negative(even, input_x, input_y, labels)

    # Saving x, y and labels
    np.save('input_x.npy', input_x)
    np.save('input_y.npy', input_y)
    np.save('labels.npy', labels)





