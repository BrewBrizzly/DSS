---Information-on-pre-processing---

1) Copying contains all the code for copying data. Specifically, it contains the code for 
copying the parchment fragments from the complete data-set to a separate data-set.

2) The step above is performed through reading the .csv from the Parchment_Plate_Numbers directory.
This .csv contains all the names of the plates that contain parchment fragments. 

3) After, the masks are created and saved for each parchment fragment by using the Matlab code from the Create_Masks directory. This code also extracts the fragment through the use of the mask and saves the result. 

4) Having obtained a data-set of isolated parchment fragments, patches are extracted from each fragment via the code in the Create_Patches directory. A patch is only saved when it contains at least one non-black pixel in the image. This serves as a baseline data-set. 

5) Now the Extract_Patches directory is used for creating a numpy array containing arrays of all the the paths to patches, that meet the set cutoff requirement, belonging to the same bin. In paralel, a numpy array is created containing all the bin values. So the both structs are in ordered by the bin-values. 

6) At last, the appropriate structure for training the self-supervised siamese model is created via the code in the Create_Pairs directory. All the possible positive and negative path/patch pairs are created with an array containing the labels in paralel. For testing the self-supervised model, there is also a struct containing labels on the basis of which patch belongs to the same plate. For training, the labels are created on the basis of which patches belong to the same fragment. 



