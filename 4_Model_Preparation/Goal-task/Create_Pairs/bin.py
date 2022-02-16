import numpy as np 
from numpy import genfromtxt
import csv
import matplotlib.pyplot as plt
import random 


# First filter and then bin the fragment patches on Q-number 
def bin_Q(Path_Q, Path_P, Path_SP):

    # Lists to store csv in 
    ls_plate = []
    ls_q = []

    # Store the Q nnumber in a list 
    with open(Path_Q, 'r') as file: 
        csv_struct = csv.reader(file) 

        for plate in csv_struct:
            ls_q.append(plate[0])

    # Store the coherent paths in a list 
    with open(Path_P, 'r') as file: 
        csv_struct = csv.reader(file) 

        for plate in csv_struct:
            ls_plate.append(plate[0])

    # Pairing the two lists, so the plate with its q-number
    ls = list(zip(ls_plate, ls_q))

    # Read the array containing the sorted test paths of patches 
    arr = np.load(Path_SP, allow_pickle = True)

    # Obtain only plates, and therefore fragments, that exist in both structs 
    ls_fragments = filter_fragments(arr, ls_plate)

    # A list containing the Q number for each fragment instance in ls_fragments 
    ls_Q = filter_Q(ls_fragments, ls)

    # Bin the fragment belonging together on the basis of their Q-number
    ls_frag_bin = bin(ls_fragments, ls_Q)

    # Creating a plot of the frequency of the amount fragments per Q-number
    plot_Q(ls_frag_bin)

    # Creating pairs 
    input_x, input_y, labels = create_pairs(ls_frag_bin)

    # Saving the lists
    np.save('input_x.npy', input_x)
    np.save('input_y.npy', input_y)
    np.save('labels.npy', labels)


# Delete plates that are not in both structs 
def filter_fragments(arr, ls_plate):

    # list for filtered fragments 
    ls_fragments = []

    # For bin array
    for bn in arr:

    	# For fragment in bin
        for frag in bn:

        	# For path in fragment 
            for path in frag:

            	# Splitting the string to get the plate of the patch 
                string = path  

                string = string.rsplit('/', 1)[1]
                string = string.split('-')[0]

                if 'P' in string:
                    string = string.split('P')[1]

                # If plate in both structs, append to list 
                if string in ls_plate:
                    ls_fragments.append(frag)
                    break 

    return ls_fragments 


# Assign each instance in ls_frag its q_number in a separate list 
def filter_Q(ls_frag, ls):

    ls_Q = []

    # For fragment in list 
    for frag in ls_frag:

    	# For path in fragment 
        for path in frag:

        	# Splitting the string to get the plate of the patch, and therefore fragment  
            string = path  

            string = string.rsplit('/', 1)[1]
            string = string.split('-')[0]

            if 'P' in string:
                string = string.split('P')[1]

            # For pair of plate and q-number in list 
            for pair in ls:

            	# If plate in pair 
                if string in pair:

                	# Append the Q-number to the list 
                    ls_Q.append(pair[1])
            break 

    return ls_Q


# Creates a list of lists containing the fragments that belong together according to the Q-number
def bin(ls_frag, ls_q):

    # Creating a list to store all fragment that belong to the same bin 
    ls_frag_bin = []    

    # Creating a list of all unique Q numbers
    set_q = set(ls_q)

    # For each unique Q-number
    for unq_q in set_q:

    	# Temporary list to store all fragment with the same Q-number
        tmp_bin = []

        # Loop through the fragments and their q-numbers
        for fragment, q_number in zip(ls_frag, ls_q):
            
            # When a bin is found 
            if unq_q == q_number:

                tmp_bin.append(fragment)

        ls_frag_bin.append(tmp_bin)

    return ls_frag_bin


# Creating a plot of the frequency of the amount fragments per Q-number
def plot_Q(ls_frag_bin):

    # List for the amount of fragments per instance 
    len_ls = []

    # Determining amount of fragments per instance that have more than 1 fragment 
    for bn in ls_frag_bin:
        if len(bn) != 1:
            len_ls.append(len(bn))

    # Determine x axis for barplot 
    x = np.unique(len_ls)

    # Convert ints to strings
    str_x = [str(intg) for intg in x]

    # Determine y axis
    y = []
    for x_unq in x:
        cnt = 0 
        for vl in len_ls:
            if x_unq == vl:
                cnt += 1
        y.append(cnt)

    # Creating the figure and axis 
    fig, axs = plt.subplots(1, 1)
    axs.bar(str_x, y, edgecolor='black', linewidth=1.0)
    axs.set_xlabel('Total number of fragments per Q-number')
    axs.set_ylabel('Frequency')

    plt.savefig('q_dist.png')
    plt.close()


# Creating the positive and negative pairs for testing on Q-numbers 
def create_pairs(ls_frag_bin):

    # array to store only q-number bins with length more than 1        
    tmp = []
    
    # Removing all the Q-number bins that contain only one fragment
    for q_bn in ls_frag_bin:
        if len(q_bn) != 1:
            tmp.append(q_bn)         

    # Create positive pairs 
    pos_a = []
    pos_b = []
    pos_a, pos_b, pos_lbl = create_pos(tmp)

    # Creating negative pairs
    neg_a = []
    neg_b = []
    neg_a, neg_b, neg_lbl = create_neg(tmp, len(pos_a))

    # Concat both lists 
    input_a = pos_a + neg_a 
    input_b = pos_b + neg_b
    labels = pos_lbl + neg_lbl

    return input_a, input_b, labels


# Creating the positive pairs 
def create_pos(ls):

    # Lists for storing postive pairs 
    pos_a = []
    pos_b = [] 

    # For qnumber bin in list 
    for q in ls:

        # Base fragment of a qnumber bin 
        frag1 = q[0]

        # Fragments to pair the base fragment with in the current bin  
        for idx in range(len(q) - 1):
            idx += 1
            frag2 = q[idx]

            # Take a random patch from each fragment to create a pair 
            pos_a.append(random.choice(frag1))
            pos_b.append(random.choice(frag2))

    # Creating a list of  positivelabels 
    pos_lbl = np.ones(len(pos_a))

    return pos_a, pos_b, pos_lbl.tolist()

# Creating the negative pairs 
def create_neg(ls, max_len):

    # Lists for storing negative pairs 
    neg_a = []
    neg_b = [] 

    # Defining the starting indexes to loop from both ends of the list 
    begin = 0
    end = len(ls) - 1

    # While we have not reached the length of the positive pairs or the list is exhausted in terms of pairing 
    while(len(neg_a) != max_len) and begin != end:

        # i begins from the left and j from the right of the list 
        i = begin
        j = end

        # While item i is equal to item j or 
        # length positive pair is equal to negative pair 
        while(int(i) != int(j)) and (len(neg_a) != max_len) and i < j:

            # Grabbing the q bins from left and right 
            q_bin1 = ls[i]
            q_bin2 = ls[j]

            # Grabbing a random fragment from a bot left and right q bin 
            frag1 = random.choice(q_bin1)
            frag2 = random.choice(q_bin1)

            # Grabbing a random patch from each fragment for pairing 
            neg_a.append(random.choice(frag1))
            neg_b.append(random.choice(frag2))
            i += 1 
            j -= 1 

        # Make sure that each pair is unique 
        begin += 1

    # Creating a list of negative labels 
    neg_lbl = np.zeros(len(neg_a))

    return neg_a, neg_b, neg_lbl.tolist()












