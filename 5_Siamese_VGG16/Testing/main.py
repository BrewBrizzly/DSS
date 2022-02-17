# Script for measuring performance of 
# trained model 

# Required libraries 
from test import *

def main():

    # Path to trained model 
    path = 'VGG16.h5'

    # Paths to test data
    A1 = '/data/p301438/Data/Q_numbers_opt/Positive/A/*.jpg'
    B1 = '/data/p301438/Data/Q_numbers_opt/Positive/B/*.jpg'
    A0 = '/data/p301438/Data/Q_numbers_opt/Negative/A/*.jpg'
    B0 = '/data/p301438/Data/Q_numbers_opt/Negative/B/*.jpg'

    # Testing the trained model
    test_model(path, A1, B1, A0, B0)

if __name__ == '__main__':

    main()