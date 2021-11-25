# Returns amount of fragments 

# Modules
import os 

def get_number(path):
    
    n_fragments = [] 
    for plate in os.listdir(path):
        n_fragments.append(len(plate))

    print("Number of plates: " , len(n_fragments))
    print("Number of fragments: " , sum(n_fragments))