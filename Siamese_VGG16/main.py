# This script loads the dirs into tensors,
# creates the labels, builds a Siamese VGG16,
# And fits the data to the model to train and validate it.

# Required libraries
from model import *

def main():
    dir_A = '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15/Training-Validation/A/'
    dir_B = '/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15/Training-Validation/B/'
    train(dir_A, dir_B)


if __name__ == '__main__':

    main()