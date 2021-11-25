# Contains statistical methods

# Modules
import os 
import numpy as np 
import matplotlib.pyplot as plt

class statistic(object):

    def __init__(self, path, np_count_exists):
        self.path = path
        self.total_patches = None
        self.arr_patches_per_fragment = None
        if np_count_exists:
            self.set_arr_patches_per_fragment()
            self.set_total_patches() 
        else:
            self.make_arr_patches_per_fragment()


    # creates a list where each index is the amount of patches for a fragment 
    def make_arr_patches_per_fragment(self):

        # Temporary list
        tmp_ls = [] 

        # Looping throught the dir 
        for plate in os.listdir(self.path):
            plate = os.path.join(self.path, plate)
            print("Checking plate")
            for fragment in os.listdir(plate):
                fragment = os.path.join(plate, fragment)
                tmp_ls.append(len(os.listdir(fragment)))
        
        # Converting array to numpy
        self.arr_patches_per_fragment = np.asarray(tmp_ls)

        # Setting the amount of patches 
        self.set_total_patches()

        # Saving the numpy array
        self.save_np()

    def make_hist(self):
        unique = np.sort(np.unique(self.arr_patches_per_fragment))
        fig,ax = plt.subplots(1,1)
        ax.hist(self.arr_patches_per_fragment, bins = unique, edgecolor='black', linewidth=1.0)
        ax.set_title("number of patches per number of fragments")
        ax.set_xticks(unique)
        ax.set_xlabel('number of patches')
        ax.set_ylabel('number of fragments')
        plt.figtext(0.55, 0.7, "Total patches: " + str(self.total_patches))
        plt.savefig('10_percent_cutoff/occurence.png')


    def set_total_patches(self):
        self.total_patches = sum(self.arr_patches_per_fragment)
    

    def get_total_patches(self):
        return self.total_patches


    def set_arr_patches_per_fragment(self):
        self.arr_patches_per_fragment = np.load('10_percent_cutoff/patches_per_fragment.npy')


    def get_arr_patches_per_fragment(self):
        return self.arr_patches_per_fragment


    def save_np(self):
        np.save('patches_per_fragment', self.arr_patches_per_fragment)
    



