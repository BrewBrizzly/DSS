# Filter and bin belonging fragment on basis of Q-numbers

# Required lib 
from bin import * 

def main():

	# Path to sorted csv of plate numbers
	Path_Q = '/Users/stephannijdam/Desktop/Temp_Q/csv/Q-numbers.csv'

	# Path to sorted csv of Q-numbers
	Path_P = '/Users/stephannijdam/Desktop/Temp_Q/csv/Plate.csv'

	# Path to sorted and splitted testing data 
	Path_SP = '/Users/stephannijdam/Desktop/Temp_Q/test/Testing.npy'	

	# Filter and bin the belonging fragment patches into one array 
	bin_Q(Path_Q, Path_P, Path_SP)




if __name__ == '__main__':
	main()