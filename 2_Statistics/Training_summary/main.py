# Script that creates a plot containing the losses over epochs 
# during training of the model 

# Required libraries
from plot import create_plot

def main():

	# Path to numpy array containing the losses during training
	path = '/Users/stephannijdam/Desktop/DSS/5_Siamese_VGG16/VGG16_losses.npy' 

	# Creating the ploth
	create_plot(path)

if __name__ == '__main__':
	main()