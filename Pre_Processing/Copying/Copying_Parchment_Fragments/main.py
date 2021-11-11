# Copying the plates directory from source if plate contains
# Leather fragments.

# Files
from copy_fragments import *

# Defining globals
global source 
source = '/projects/mdhali/BscProjects/data/IAAfragments_onlyColor-resized50/'

global dest 
dest = '/projects/mdhali/BscProjects/Stephan/IAAfragments_parchment_onlyColor-resized50' 

global csv_path 
csv_path = '/home/s3690970/Desktop/Bachelor_Project/DSS/Pre_Processing/Parchment_Plate_Numbers/Leather-Plates.csv'


def main():

	copy_fragments(source, dest, csv_path)

if __name__ == '__main__':
	main()