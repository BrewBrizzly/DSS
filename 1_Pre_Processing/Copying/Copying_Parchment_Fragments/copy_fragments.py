# Creating dir and copying content if leather fragment

# Modules 
import os, sys, csv 

# Creating the directories and copying content 
def copy_content(source, dest, plate):
	try:
		os.system("rsync -avP " + source + plate + " " + dest)
	except:
		print("Dir is already present: " + plate)

# Hardcoded exception cases in current csv
def exception(obj):
	if obj == '623-626-630':
		obj = '623,626,630'
	if obj == '629-621':
		obj = '629,621'
	if obj == '520.526':
		obj = '520,526'
	if obj == '520.526-1':
		obj = '520,526-1'
	return obj 

# Downsizing dim of obj
def downsize(obj):
	return obj[0]

def copy_fragments(source, dest, csv_path):

	with open(csv_path, 'r') as file: 
		csv_struct = csv.reader(file) 

		# Looping through all the plate numbers in csv_struct
		for plate in csv_struct:

			# Downsizing dim 
			plate = downsize(plate) 

			# Two exception cases in the csv with regards to , 
			plate = exception(plate)

			# Creating and copying dir 
			copy_content(source, dest, plate)


