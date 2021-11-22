# Converting integer to unix suitable string 

def convert(integer):
	convention = string(integer)
	if integer < 10:
		convention = '00' + convention
	if integer > 9 and integer < 100:
		convention = '0' + convention
	return convention