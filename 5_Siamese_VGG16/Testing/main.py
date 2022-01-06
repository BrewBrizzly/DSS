# Script for measuring performance of 
# trained model 

# Required libraries 
from test import *

def main():

    # Path to trained model 
    path = '/projects/mdhali/BscProjects/Stephan/Model/14_epochs/VGG16.h5'

    # Paths to test data
    A1 = '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15/Testing/Positive/A/'
    B1 = '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15/Testing/Positive/B/'
    A0 = '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15/Testing/Negative/A/'
    B0 = '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15/Testing/Negative/B/'

    # Testing the trained model
    test_model(path, A1, B1, A0, B0)

if __name__ == '__name__':
    main()