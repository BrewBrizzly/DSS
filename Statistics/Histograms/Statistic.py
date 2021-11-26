# Contains statistical methods

# Modules
import os 
import numpy as np 
import matplotlib.pyplot as plt

class statistic(object):

    def __init__(self, path):
        self.path = path
        
    # Creates all the histograms for each list 
    def make_histogram(self):

        # Temporary list to create one general histogram
        tmp_frag = []
        tmp_patch = []
        tmp_cutoff = []

        # Looping through all the lists 
        for list_name in os.listdir(self.path):
            list_path = os.path.join(self.path, list_name)

            # Check if it is a npy file 
            if list_name.endswith('.npy'):

                # Load the numpy list 
                arr = np.load(list_path)

                # Converting for the plot to ls
                ls = arr.tolist()

                # Removing zero values 
                ls = self.remove_value_ls(ls, 0)

                # Removing 1 values 
                ls = self.remove_value_ls(ls, 1)

                # Getting each unique bin for the plot  
                bins = np.unique(ls)

                # Checking if there is a bin value 
                if bins.any():

                    # Name of the plot 
                    name = list_name.split('.npy')[0]

                    # Counting all the patches that meet the cutoff 
                    cnt_patches = sum(ls)

                    # Getting all the other coutns for plot
                    cnt_fragments = len(ls)

                    # Current cutoff value 
                    cutoff = name.split('_')[2]

                    # Plotting and saving the histrogram of the list
                    self.plt_histogram_unq(ls, bins, name, cnt_patches, cnt_fragments, cutoff)

                    # Saving the values in list 
                    tmp_frag.append(cnt_fragments)
                    tmp_patch.append(cnt_patches)
                    tmp_cutoff.append(int(cutoff))

        self.plt_histogram_gen(tmp_frag, tmp_cutoff, 'fragments.png' )
        self.plt_histogram_gen(tmp_patch, tmp_cutoff, 'patches.png')




    def plt_histogram_unq(self, ls, bins, name, cnt_patches, cnt_fragments, cutoff):

        # Plotting the histogram 

        # Creating the figure and axis 
        fig, axs = plt.subplots(1, 1)

        # Adding the hist values to the axis 
        axs.hist(ls, bins, edgecolor='black', linewidth=1.0)

        # Setting the ticks for the hist
        axs.set_xticks(bins)

        # Setting the labels for the axis 
        axs.set_xlabel('number of patches per fragment')
        axs.set_ylabel('number of patches')

        # Adding texts to the figure 
        plt.figtext(0.55, 0.75, "Cutoff at: " + cutoff + '%')
        plt.figtext(0.55, 0.70, "total patches: " + str(cnt_patches))
        plt.figtext(0.55, 0.65, "total fragments: " + str(cnt_fragments))
        plt.savefig('Images/Unique/' + name + '.png')
        plt.close()    

    def plt_histogram_gen(self, ls, bins, name):
        print(ls)
        print(bins)

    def remove_value_ls(self, ls, value):
        if value in ls:
            ls = list(filter(lambda x: x != value, ls))
        return ls

            




    # # creates a list where each index is the amount of patches for a fragment 
    # def make_arr_patches_per_fragment(self):

    #     # Temporary list
    #     tmp_ls = [] 

    #     # Looping throught the dir 
    #     for plate in os.listdir(self.path):
    #         plate = os.path.join(self.path, plate)
    #         print("Checking plate")
    #         for fragment in os.listdir(plate):
    #             fragment = os.path.join(plate, fragment)
    #             tmp_ls.append(len(os.listdir(fragment)))
        
    #     # Converting array to numpy
    #     self.arr_patches_per_fragment = np.asarray(tmp_ls)

    #     # Setting the amount of patches 
    #     self.set_total_patches()

    #     # Saving the numpy array
    #     self.save_np()

    # def make_hist(self):
    #     unique = np.sort(np.unique(self.arr_patches_per_fragment))
    #     fig,ax = plt.subplots(1,1)
    #     ax.hist(self.arr_patches_per_fragment, bins = unique, edgecolor='black', linewidth=1.0)
    #     ax.set_title("number of patches per number of fragments")
    #     ax.set_xticks(unique)
    #     ax.set_xlabel('number of patches')
    #     ax.set_ylabel('number of fragments')
    #     plt.figtext(0.55, 0.7, "Total patches: " + str(self.total_patches))
    #     plt.savefig('10_percent_cutoff/occurence.png')


    # def set_total_patches(self):
    #     self.total_patches = sum(self.arr_patches_per_fragment)
    

    # def get_total_patches(self):
    #     return self.total_patches


    # def set_arr_patches_per_fragment(self):
    #     self.arr_patches_per_fragment = np.load('10_percent_cutoff/patches_per_fragment.npy')


    # def get_arr_patches_per_fragment(self):
    #     return self.arr_patches_per_fragment


    # def save_np(self):
    #     np.save('patches_per_fragment', self.arr_patches_per_fragment)
    



