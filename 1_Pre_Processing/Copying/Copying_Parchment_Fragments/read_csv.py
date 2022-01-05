# Reading and return csv as struct 

# Modules
import csv

# Reading and returning the csv as struct 
def read_csv(path):
	with open(path, 'r') as file: 
		csv_struct = csv.reader(file)
		return csv_struct 

