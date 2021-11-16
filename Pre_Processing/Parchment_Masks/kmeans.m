% Possible parameters depending on system

% myFolder = '/data/p301438/IAAfragments_parchment_onlyColor-resized50';
% myFolder = '/projects/mdhali/BscProjects/Stephan/IAAfragments_parchment_onlyColor-resized50';
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

% Possible dir for Binarized image

% Binarized_path =  ['/data/p301438/IAAfragments_onlyBinarized/', newDir ,'/', extractBefore(baseFileName, '-D'), '.jpg'];


% Below the actual code 

% Specify the folder where the files live.

myFolder = 'D:\Bproject\fragments';

% File pattern, in this case .jpg

filePattern = fullfile(myFolder, '**\*.jpg');

% List of all the names of the files that match pattern

theFiles = dir(filePattern);

for k = 1 : length(theFiles)

    % Determine the path to the fragment

    baseFileName = theFiles(k).name;
    fullFileName = fullfile(theFiles(k).folder, baseFileName);

    % Getting the dir to store the mask, fragment and the path to the
    % binarized image

    position = find(theFiles(k).folder == '\', 1, 'last');
    newDir = extractAfter(theFiles(k).folder, position);
    
    % Dir for extracted frag  

    Dir_frag = ['D:\Bproject\IAAfragments_isolated_parchment_onlyColor-resized50\', newDir];

    % Dir for extracted mask 

    Dir_mask = ['D:\Bproject\IAAfragments_parchment_mask_onlyColor-resized50\', newDir];
    
    % Path to binarized image 

    Binarized_path =  ['D:\Bproject\Binarized\IAAfragments_onlyBinarized\', newDir ,'\', extractBefore(baseFileName, '-D'), '.jpg'];

    % Reading the fragment

    I = imread(fullFileName);

    % Converting grayscale fragment image to binarized

    BW1 = im2bw(I, 0.25);
    
    % Removing small white pixels before image-infilling 

    BW2 = bwareaopen(BW1, 50);
    
    % Filling black holes in the mask, most likely text  

    BW3 = imfill(BW2, 'holes');

    % Removing larger white left-overs after image-infilling 
    BW4 = bwareaopen(BW1, 600);

    % Code lines 60 to 83 for grabbing the object closest to the center of the image
    % obtained from https://nl.mathworks.com/matlabcentral/answers/797442-find-the-object-closest-to-the-center

    [rows, columns] = size(BW4);
    [labeledImage, numBlobs] = bwlabel(BW4);

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

    % Reading corresponding binarized image, if it exists to extend the
    % mask
    if isfile(Binarized_path)

        Binarized_image = imread(Binarized_path);
    
        % Converting the binarized image to binary format 
        B2 = im2bw(Binarized_image, 0.5);
        
        % Taking the inverse of the binarized image since we want to 
        % add the text to the mask 
        B3 = 1 - B2;
        
        % Combining the orignal Mask with the binarized image 
        Mask = bitor(Mask, B3);

    end
    
    % Combining the mask and fragment

    Res = bsxfun(@times, I, cast(Mask, 'like', I));

    % Create dir for frag if not exist 

    if ~exist(Dir_frag, 'dir')
       mkdir(Dir_frag)
    end

    % Saving the 50 percent downscaled combination of fragment and mask 

    imwrite(Res, [Dir_frag,'\', baseFileName]);

     % Create dir for mask if not exist 

    if ~exist(Dir_mask, 'dir')
       mkdir(Dir_mask)
    end
    
    % Saving the mask
    
    imwrite(Mask, [Dir_mask,'\', baseFileName]);

end
