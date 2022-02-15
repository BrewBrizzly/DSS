# This script loads the dirs into tensors,
# creates the labels, builds a Siamese VGG16,
# And fits the data to the model to train and validate it.

# Required libraries
from model import *

def main():

    # Paths to postive pairs and negative pairs
    Path_Positive_A = '/data/p301438/Data/Training/Positive/A/*.jpg'
    Path_Positive_B = '/data/p301438/Data/Training/Positive/B/*.jpg'

    Path_Negative_A = '/data/p301438/Data/Training/Negative/A/*.jpg'
    Path_Negative_B = '/data/p301438/Data/Training/Negative/B/*.jpg'
    
    # Processing the data, creating and training the model with the data
    run_model(Path_Positive_A, Path_Positive_B, Path_Negative_A, Path_Negative_B)


if __name__ == '__main__':

    main()