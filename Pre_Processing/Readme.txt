---Information-on-pre-processing---

1) Copying contains all the code for copying data. Specifically, it contains the code for 
copying the parchment fragments from the complete data-set to a separate data-set.

2) The step above is performed through reading the .csv from the Parchment_Plate_Numbers directory.
This .csv contains all the names of the plates that contain parchment fragments. 

3) After, the masks are created and saved for each parchment fragment by using the Matlab code from the Create_Masks directory. This code also extracts the fragment through the use of the mask and saves the result. 

4) Having obtained a data-set of isolated parchment fragments, patches are extracted from each fragment via the code in the Create_Patches directory. A patch is only saved when it contains at least one non-black pixel in the image. This serves as a baseline data-set. 



