# Contains statistical methods for information on the patches extracted 

# Modules
import os 
import numpy as np 
import matplotlib.pyplot as plt

class statistic(object):

    def __init__(self, path):
        self.path = path
        self.cnt_fragments = []
        self.cnt_patches = []
        self.trk_cutoff = [] 
        
    # Creates all the histograms for each list 
    def make_histogram(self):

        # Looping through all the lists 
        for list_name in os.listdir(self.path):
            list_path = os.path.join(self.path, list_name)

            # Check if it is a npy file 
            if list_name.endswith('.npy'):

                # Load the numpy list 
                arr = np.load(list_path)

                # Converting arr for the plot to list
                ls = arr.tolist()

                # Removing zero values fron list
                ls = self.remove_value_ls(ls, 0)

                # Removing 1 values from list 
                ls = self.remove_value_ls(ls, 1)

                # Name of the plot 
                name = list_name.split('.npy')[0]

                # Current cutoff value 
                cutoff = name.split('_')[2]

                # Tracking the current cutoff 
                self.trk_cutoff.append(cutoff)

                # Getting each unique bin for the plot  
                bins = np.unique(ls)

                # Checking if there is a bin value
                if bins.any():

                    # Counting all the patches that meet the cutoff 
                    cnt_patches = sum(ls)

                    # Getting all the other coutns for plot
                    cnt_fragments = len(ls)

                    # Plotting and saving the histrogram of the list
                    self.plt_histogram_unq(ls, bins, name, cnt_patches, cnt_fragments, cutoff)

                    # Tracking the patches and fragments 
                    self.cnt_fragments.append(cnt_fragments)
                    self.cnt_patches.append(cnt_patches)

                # Keeping track of the empy bins fragments and patches 
                else:
                    self.cnt_fragments.append(0)
                    self.cnt_patches.append(0)


    def plt_histogram_unq(self, ls, bins, name, cnt_patches, cnt_fragments, cutoff):

        # Plotting the histogram 

        # Creating the figure and axis 
        fig, axs = plt.subplots(1, 1)

        # Adding the hist values to the axis 
        axs.hist(ls, bins, edgecolor='black', linewidth=1.0)

        # Setting the ticks for the hist
        axs.set_xticks(bins)

        # Setting the labels for the axis 
        axs.set_xlabel('Total number of patches in fragment')
        axs.set_ylabel('Number of fragments')

        # Adding texts to the figure 
        plt.figtext(0.55, 0.75, "Cutoff at: " + cutoff + '%')
        plt.figtext(0.55, 0.70, "Total patches: " + str(cnt_patches))
        plt.figtext(0.55, 0.65, "Total fragments: " + str(cnt_fragments))
        plt.savefig('Images/Unique/' + name + '.png')
        plt.close()    


    # Making an overall summary of the patches and fragments accepted 
    def make_summary(self):

        # Making sure that the lists are ordered by bins  
        self.sort()

        # Plotting summary 
        self.plotter()

    # Sorting the lists in order of bins 
    def sort(self):

        # Defining our stop value 
        # The length of the list
        stop = len(self.trk_cutoff)

        # For index and object in our trk_cutoff
        for idx1, obj in enumerate(self.trk_cutoff):

            # Comparing index 
            idx2 = idx1 + 1 

            # Comparing till the stop 
            while(idx2 != stop):
                
                # Object in the list to compare to 
                cmp_obj = self.trk_cutoff[idx2]

                # Swap if object is larget than comparison obj
                if int(obj) > int(cmp_obj):

                    # Order the bins 
                    self.trk_cutoff[idx1] = cmp_obj
                    self.trk_cutoff[idx2] = obj

                    # Order the other two lists acc. 
                    tmp1 = self.cnt_fragments[idx1] 
                    tmp2 = self.cnt_fragments[idx2]

                    self.cnt_fragments[idx1] = tmp2
                    self.cnt_fragments[idx2] = tmp1

                    tmp1 = self.cnt_patches[idx1] 
                    tmp2 = self.cnt_patches[idx2]

                    self.cnt_patches[idx1] = tmp2
                    self.cnt_patches[idx2] = tmp1

                    obj = cmp_obj

                # Increase idx2
                idx2 += 1 

    def plotter(self):

        # Creating the figure and axis 
        fig, axs = plt.subplots(1, 1)

        # Adding the hist values to the axis 
        axs.plot(self.trk_cutoff, self.cnt_fragments, label = 'Fragments', linewidth = 1.0)
        axs.plot(self.trk_cutoff, self.cnt_patches, label = 'Patches', linewidth = 1.0)

        # Adding a limit and grid 
        axs.set_xlim(self.trk_cutoff[0], self.trk_cutoff[-1])
        axs.set_ylim(0,)
        axs.grid()

        # Setting the labels for the axis 
        axs.set_xlabel('Percentage of fragment in image')
        axs.set_ylabel('Occurence')
        axs.legend()

        # Adding texts to the figure 
        plt.savefig('Images/Summary/' + 'summary' + '.png')
        plt.close()

    def remove_value_ls(self, ls, value):
        if value in ls:
            ls = list(filter(lambda x: x != value, ls))
        return ls
    



