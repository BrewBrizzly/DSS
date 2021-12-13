# Splitting the array of paths
# Into 80% Training/Validation and 
# 20% Testing

# Requiered library
from split import *

def main():

	# Path to the array
	path = ''

	# Splitting the data in prefered in set manner
	split_data(path, 0.8)

if __name__ == '__main__':
	main()