% Specify the folder where the files live.
% myFolder = '/data/p301438/IAAfragments_onlyColor-resized50';
% myFolder = '/projects/mdhali/BscProjects/Stephan/IAAfragments_parchment_onlyColor-resized50/';
myFolder = '/Users/stephannijdam/Desktop/DSS/Pre_Processing/Parchment_Masks';

% File pattern, in this case .jpg
% filePattern = fullfile(myFolder, '**/*.jpg');
filePattern = fullfile(myFolder, '*.jpg');

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
    
    % Converting every value 2 to 255
    L(L==2)=255;
    
    % Converting grayscale image to binarized
    BW1 = im2bw(L,0.5);
    
    % Filling holes in mask
    BW2 = imfill(BW1,'holes');

    % Code lines 38 to  for grabbing the object closest to the center of the image
    % https://nl.mathworks.com/matlabcentral/answers/797442-find-the-object-closest-to-the-center
    [rows, columns] = size(BW2);
    [labeledImage, numBlobs] = bwlabel(BW2);

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
    Mask = ismember(labeledImage, sortOrder(1:2));
    
    % Combining the mask and fragment
    Res = bsxfun(@times, I, cast(Mask, 'like', I));
    
    % Getting string value of k 
    % stringK = int2str(k);

    % Getting the dir to store the mask and fragment 
    position = find(theFiles(k).folder == '/', 1, 'last');
    newDir = extractAfter(theFiles(k).folder, position);
    
    % Dir for extracted mask 
    % Dir_frag = ['/data/p301438/IAAfragments_isolated_parchment_onlyColor-resized50/', newDir];
    % Dir_frag = ['/projects/mdhali/BscProjects/Stephan/IAAfragments_isolated_parchment_onlyColor-resized50/', newDir];
    Dir_frag = ['/Users/stephannijdam/Desktop/test/frag/', newDir];
    mkdir(Dir_frag)

    % Saving the 50 percent downscaled combination of fragment and mask 
    %imwrite(Res, ['/data/p301438/IAAfragments_isolated_parchment_onlyColor-resized50/', newDir ,'/', baseFileName]);
    %imwrite(Res, ['/projects/mdhali/BscProjects/Stephan/IAAfragments_isolated_parchment_onlyColor-resized50/', newDir, '/', baseFileName]);
    imwrite(Res, ['/Users/stephannijdam/Desktop/test/frag/', newDir, '/', baseFileName]);
    
    % Dir for extracted mask ;
    % Dir_mask = ['/data/p301438/IAAfragments_parchment_mask_onlyColor-resized50/', newDir];
    Dir_mask = ['/Users/stephannijdam/Desktop/test/mask/', newDir];
    mkdir(Dir_mask);
    
    % Saving the mask 
    % imwrite(Mask, ['/data/p301438/IAAfragments_parchment_mask_onlyColor-resized50/', newDir ,'/', baseFileName]);
    % imwrite(Mask, ['/projects/mdhali/BscProjects/Stephan/IAAfragments_parchment_mask_onlyColor-resized50/', newDir, '/', baseFileName]);
    imwrite(Mask, ['/Users/stephannijdam/Desktop/test/mask/', newDir, '/', baseFileName])

end
