# Filter and bin belonging fragment on basis of Q-numbers

# Required lib 
from bin import * 

def main():

	# Path to sorted csv of plate numbers
	Path_Q = '/Users/stephannijdam/Desktop/Temp_Q/Q_Number_csv/Q-numbers.csv'

	# Path to sorted csv of Q-numbers
	Path_P = '/Users/stephannijdam/Desktop/Temp_Q/Q_Number_csv/Plate.csv'

	# Path to sorted and splitted testing data 
	Path_SP = '/Users/stephannijdam/Desktop/Temp_Q/Testing_Data_Paths/Testing.npy'	

	# Filter and bin the belonging fragment patches into one array 
	bin_Q(Path_Q, Path_P, Path_SP)




if __name__ == '__main__':
	main()