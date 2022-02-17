# Alter the labels 

# Required lib 
from bin import * 

def main():

	# Path to sorted csv of plate numbers
	Path_Q = 'Q-numbers.csv'

	# Path to sorted csv of Q-numbers
	Path_P = 'Plate.csv'

	# Path to sorted and splitted testing data 
	Path_SP = 'Testing.npy'	

	# Filter and bin the belonging fragment patches into one array 
	bin_Q(Path_Q, Path_P, Path_SP)


if __name__ == '__main__':
	main()