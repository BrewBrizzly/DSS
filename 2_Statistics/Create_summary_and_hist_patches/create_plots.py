import numpy as np 
import os 
import matplotlib.pyplot as plt


def loop_arrays(path):

    summary_patch = []
    summary_frag = []
    bins = []

    # Looping through all the arrays
    for ls_file in os.listdir(path):

        ls_path = os.path.join(path, ls_file)

        # Loading the array as numpy
        arr = np.load(ls_path, allow_pickle = True)

        # Create the boxplot for the array, teturns summary values
        cnt_patch, cnt_fragment, name = pre_proces_plot(arr, ls_file)

        # Saving summary values
        summary_patch.append(cnt_patch)
        summary_frag.append(cnt_fragment)
        bins.append(name)

    # Sort the summary before plotting
    summary_sort(summary_patch, summary_frag, bins)



def pre_proces_plot(arr, ls_file):

    # Creating a list of len of each item in array
    len_ls = create_len_list(arr)

    # Getting the unique bins
    bins = np.unique(len_ls)

    # Calculating the total amount of patches
    cnt_patch = sum(len_ls)

    # Calculating the total amount of fragments
    cnt_fragments = len(len_ls)

    # Getting the name of the list
    name = ls_file.split('Paths_')[1]
    name = name.split('.npy')[0]


    create_box_plot(len_ls, bins, cnt_patch, cnt_fragments, name)

    return cnt_patch, cnt_fragments, name 


def create_box_plot(len_ls, bins, cnt_patch, cnt_fragments, name):

    # Plotting the histogram 

    # Creating the figure and axis 
    fig, axs = plt.subplots(1, 1)

    # Adding the hist values to the axis 
    axs.hist(len_ls, bins, edgecolor='black', linewidth=1.0)

    # Setting the ticks for the hist
    axs.set_xticks(bins)

    # Setting the labels for the axis 
    axs.set_xlabel('Total number of patches per fragment')
    axs.set_ylabel('Frequency')

    # Adding texts to the figure 
    plt.figtext(0.55, 0.75, "Cutoff at: " + name + '%')
    plt.figtext(0.55, 0.70, "Total patches: " + str(cnt_patch))
    plt.figtext(0.55, 0.65, "Total fragments: " + str(cnt_fragments))
    plt.savefig('Images/Plots/Plot_' + name + '.png')
    plt.close()


def create_len_list(arr):
    len_ls = []

    for inst in arr:
        len_ls.append(len(inst))

    return len_ls


def summary_sort(ls1, ls2, bins):
    
    # Defining our stop value 
    # The length of the list
    stop = len(bins)

    # For index and object in our bins
    for idx1, obj in enumerate(bins):

        # Index for comparison object 
        idx2 = idx1 + 1 

        # Comparing till the stop 
        while(idx2 != stop):
            
            # Object in the list to compare to 
            cmp_obj = bins[idx2]

            # Swap if object is larget than comparison obj
            if int(obj) > int(cmp_obj):

                # Order the bins 
                bins[idx1] = cmp_obj
                bins[idx2] = obj

                # Order the other two lists accordingly 
                tmp1 = ls1[idx1] 
                tmp2 = ls1[idx2]

                ls1[idx1] = tmp2
                ls1[idx2] = tmp1

                tmp1 = ls2[idx1] 
                tmp2 = ls2[idx2]

                ls2[idx1] = tmp2
                ls2[idx2] = tmp1

                obj = cmp_obj

            # Increase idx2
            idx2 += 1 


# Creating the summary 
def create_summary(ls1, ls2, bins):

    # Creating the figure and axis 
    fig, axs = plt.subplots(1, 1)

    # Adding the hist values to the axis 
    axs.plot(bins, ls2, label = 'Fragments', linewidth = 1.0)
    axs.plot(bins, ls1, label = 'Patches', linewidth = 1.0)

    # Adding a limit and grid 
    axs.set_xlim(self.trk_cutoff[0], self.trk_cutoff[-1])
    axs.set_ylim(0,)
    axs.grid()

    # Setting the labels for the axis 
    axs.set_xlabel('Percentage of non zero value pixels')
    axs.set_ylabel('Frequency')
    axs.legend()

    # Adding texts to the figure 
    plt.savefig('Images/Summary/' + 'summary' + '.png')
    plt.close()









