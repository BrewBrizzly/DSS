# Creating dir and copying content if leather fragment

# Modules 
import os, sys
from distutils.dir_util import copy_tree 

# Creating the directories and copying content 
def copy_content(source, dest, plate):
	try:
		os.makedirs(dest, exist_ok = True)
		copy_tree(source + plate, dest)
		print("Created and copied to Dir: " + plate)
	except:
		print("Dir is already present: " + plate)

# Hardcoded exception cases in current csv
def exception(obj):
	if obj == '623-626-630':
		obj = '623,626,630'
	if obj == '629-621':
		obj = '629,621'
	return obj 

# Downsizing dim of obj
def downsize(obj):
	return obj[0]

def copy_fragments(source, dest, csv_struct):

	# Looping through all the plate numbers in csv_struct
	for plate in csv_struct:

		# Downsizing dim 
		plate = downsize(plate) 

		# Two exception cases in the csv with regards to , 
		plate = exception(plate)

		# Creating the destination for creating the folder and copying 
		dest = dest + plate 

		# Creating and copying dir 
		copy_content(source, dest, plate)


