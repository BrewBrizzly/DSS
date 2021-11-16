% Possible folders depending on system

% myFolder = '/data/p301438/IAAfragments_onlyColor-resized50';
% myFolder = '/projects/mdhali/BscProjects/Stephan/IAAfragments_parchment_onlyColor-resized50/';
% myFolder = '/Users/stephannijdam/Desktop/DSS/Pre_Processing/Parchment_Masks';
% myFolder = 'C:\Users\Stephan\Desktop\BachelorP\DSS\Pre_Processing\Parchment_Masks';

% Possible file patterns depending on system 

% filePattern = fullfile(myFolder, '**/*.jpg');
% filePattern = fullfile(myFolder, '*.jpg');

% Possible dir for fragment depending on the system 

% Dir_frag = ['/data/p301438/IAAfragments_isolated_parchment_onlyColor-resized50/', newDir];
% Dir_frag = ['/projects/mdhali/BscProjects/Stephan/IAAfragments_isolated_parchment_onlyColor-resized50/', newDir];
% Dir_frag = ['/Users/stephannijdam/Desktop/test/frag/', newDir];
% Dir_frag = ['C:\Users\Stephan\Desktop\BachelorP\DSS\Pre_Processing\Parchment_Masks\frag\', newDir];

% Possbile dir for mask depending on the system 

% Dir_mask = ['/data/p301438/IAAfragments_parchment_mask_onlyColor-resized50/', newDir];
% Dir_mask = ['/projects/mdhali/BscProjects/Stephan/IAAfragments_parchment_mask_onlyColor-resized50/', newDir];
% Dir_mask = ['/Users/stephannijdam/Desktop/test/mask/', newDir];
% Dir_mask = ['C:\Users\Stephan\Desktop\BachelorP\DSS\Pre_Processing\Parchment_Masks\mask\', newDir];

% Specify the folder where the files live.

myFolder = 'C:\Users\Stephan\Desktop\BachelorP\DSS\Pre_Processing\Parchment_Masks';

% File pattern, in this case .jpg

filePattern = fullfile(myFolder, '/*.jpg');

% List of all the names of the files that match pattern

theFiles = dir(filePattern);

for k = 1 : length(theFiles)

    % Determine the path to the file 

    baseFileName = theFiles(k).name;
    fullFileName = fullfile(theFiles(k).folder, baseFileName);
    
    % Reading the fragment

    I = imread(fullFileName);
    
    % Downscaling 

    I = imresize(I, 0.2, "bicubic");

    % Performing image segmentation via k-means of 2 

    [L,Centers] = imsegkmeans(I, 2);
    
    % Converting every value 2 to 255im

    L(L==2)=255;
    
    % Converting grayscale image to binarized

    BW1 = im2bw(L,0.5);
    
    % Removing small white pixels 

    BW2 = bwareaopen(BW1, 50);
    
    % Filling holes in the mask, most likely text  

    BW3 = imfill(BW2, 'holes');

    % Code lines 60 to 83 for grabbing the object closest to the center of the image
    % obtained from https://nl.mathworks.com/matlabcentral/answers/797442-find-the-object-closest-to-the-center

    [rows, columns] = size(BW3);
    [labeledImage, numBlobs] = bwlabel(BW3);

    % Measuring the centroid of each object 

    props = regionprops(labeledImage, 'Centroid');
    xy = vertcat(props.Centroid);
    x = xy(:, 1);
    y = xy(:, 2);

    % distance from object to center 

    distances = sqrt((columns/2 - x) .^ 2 + (rows/2 - y) .^ 2);

    % Sorting to get object closest to center

    [sortedDistances, sortOrder] = sort(distances, 'ascend');
   
    % Creating the mask of the object closest to center 

    Mask = ismember(labeledImage, sortOrder(1:1));
    
    % Combining the mask and fragment

    Res = bsxfun(@times, I, cast(Mask, 'like', I));

    % Getting the dir to store the mask and fragment 

    position = find(theFiles(k).folder == '\', 1, 'last');
    newDir = extractAfter(theFiles(k).folder, position);
    
    % Dir for extracted frag  

    Dir_frag = ['C:\Users\Stephan\Desktop\BachelorP\DSS\Pre_Processing\Parchment_Masks\frag\', newDir];
    mkdir(Dir_frag)

    % Saving the 50 percent downscaled combination of fragment and mask 

    imwrite(Res, [Dir_frag,'\', baseFileName]);
    
    % Dir for extracted mask 

    Dir_mask = ['C:\Users\Stephan\Desktop\BachelorP\DSS\Pre_Processing\Parchment_Masks\mask\', newDir];
    mkdir(Dir_mask);
    
    % Saving the mask
    
    imwrite(Mask, [Dir_mask,'\', baseFileName]);

end
