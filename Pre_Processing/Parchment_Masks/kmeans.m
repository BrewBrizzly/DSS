% Reading the fragment
I = imread('P193-1-Fg001-R-C01-R01-D10022016-T143025-LR445_PSC.jpg');

% Resizing the image to 50 per cent of original
I_resized = imresize(I, 0.2, "bicubic");

% Performing image segmentation via k-means of 2 
[L,Centers] = imsegkmeans(I_resized, 2);

% Converting every value 2 to 255
L(L==2)=255;

% Converting grayscale image to binarized image 
BW = im2bw(L,0.5);

% Grabbing the largest object from image 
BW = bwareafilt(BW,1);

% Filling holes in mask
Mask = imfill(BW,'holes');

% Combining the mask and fragment
Res = bsxfun(@times, I_resized, cast(Mask, 'like', I_resized));

% Saving the 50 percent downscaled combination of fragment and mask 
imwrite(Res, 'test_fragment.jpg');

% Saving the mask 
imwrite(Mask, 'test_mask.jpg')