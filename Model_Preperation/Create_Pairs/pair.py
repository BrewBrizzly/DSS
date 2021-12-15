# Creating and saving positive and 
# negative pairs

# Required modules 
import numpy as np 

# Creating the negative pair
# by going through all even fragments
# and maximizing the distance 
def create_negative(even, x, y, labels):

    # Defining the starting indexes
    begin = 0
    end = len(even) - 1

    # Setting the max length 
    max_len = 2 * len(x)

    while(len(x) != max_len) and begin != end:

        i = begin
        j = end

        # While item i is equal to item j or 
        # length even is equal to length odd
        while(int(i) != int(j)) and (len(x) != max_len) and j > 0 and i < end:

            # Creating the negative pair
            x.append(even[i])
            y.append(even[j])
            labels.append(0)
            i += 1 
            j -= 1 

    begin += 1

    # Confirmation
    print("Len even: ", (max_len / 2))
    print("Len odd:", len(x) - (max_len / 2))

    return x, y, labels


# Creating the positive pairs
# by going through odd fragments in each bin
def create_positive(arr, x, y, labels, even):

    # Looping through the bins 
    for bn in arr:

        # Confirmation
        print("bin ", len(bn[0]))

        # looping through the fragments in a bin
        for index, fragment in enumerate(bn): 

            # If even 
            if (index % 2) == 0:

                # Ensure order
                for path in fragment:

                    # extending fragment's tensors to even list 
                    even.append(path)

            # If odd
            else:

                # Defining stop loop
                stop = len(fragment)

                # Looping through all paths in fragment
                for i, path in enumerate(fragment):

                    j = i + 1 

                    # Create the pair 
                    while(j < stop):

                        # The pair 
                        x.append(path)
                        y.append(fragment[j])
                        labels.append(1)
                        j += 1

    return even, x, y, labels

# Creating both pairs
def create_pairs(path):

    # Load the array 
    arr = np.load(path, allow_pickle = True)

    # list for x and y of pair
    input_x = []
    input_y = []

    # list for the label of pair x y
    labels = []

    # Creating a list for even fragments
    even = []

    # Creating the positive pairs with odd
    even, input_x, input_y, labels = create_positive(arr, input_x, input_y, labels, even)

    # Creating the negative pairs with even
    input_x, input_y, labels = create_negative(even, input_x, input_y, labels)

    # Confirmation
    print("Len x ", len(input_x))
    print("Len y ", len(input_y))
    print("Len labels ", len(labels))

    # Saving x, y and labels
    np.save('/projects/mdhali/BscProjects/Stephan/Model_data/Paths_15/Training_validating/Paired/input_x.npy', input_x)
    np.save('/projects/mdhali/BscProjects/Stephan/Model_data/Paths_15/Training_validating/Paired/input_y.npy', input_y)
    np.save('/projects/mdhali/BscProjects/Stephan/Model_data/Paths_15/Training_validating/Paired/labels.npy', labels)





