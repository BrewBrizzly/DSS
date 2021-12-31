# This script loads the dirs into tensors,
# creates the labels, builds a Siamese VGG16,
# And fits the data to the model to train and validate it.

# Required libraries
from model import *

def main():

    # Paths
    Path_Positive_A = '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15_exp/Training/Positive/A/*.jpg'
    Path_Positive_B = '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15_exp/Training/Positive/B/*.jpg'

    Path_Negative_A = '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15_exp/Training/Negative/A/*.jpg'
    Path_Negative_B = '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15_exp/Training/Negative/B/*.jpg'
    
    run_model(Path_Positive_A, Path_Positive_B, Path_Negative_A, Path_Negative_B)


if __name__ == '__main__':

    main()