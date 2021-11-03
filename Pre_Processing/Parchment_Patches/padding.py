# Padding fragment to fit patch dimension if necassary 

# Modules 
import numpy as np 

def padding(fragment, n):

	# Taking the dimension of the fragment
	fragment_dimension = np.shape(fragment)

	# Calculating the remainder after fitting patch dimension 
	x_rem = fragment_dimension[0] % n
	y_rem = fragment_dimension[1] % n 

	# If remainder is not 0 
	if x_rem or y_rem:
		# Padding length in x and y dim
		x_incr = abs(x_rem - n) 
		y_incr = abs(y_rem - n)

		# Padding of the fragment on bottom and right 
		return np.pad(fragment, (0, x_incr), (0, y_incr))

	# If fragment already fits dimension
	else:
		return fragment

