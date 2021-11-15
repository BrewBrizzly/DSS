% Specify the folder where the files live.
% myFolder = '/data/p301438/IAAfragments_onlyColor-resized50';
myFolder = '/projects/mdhali/BscProjects/Stephan/IAAfragments_parchment_onlyColor-resized50/';

% File pattern, in this case .jpg
filePattern = fullfile(myFolder, '**/*.jpg');

% List of all the names of the files that match pattern
theFiles = dir(filePattern);

% length(theFiles)

for k = 1 : 2

    % Determine the path to the file 
    baseFileName = theFiles(k).name;
    fullFileName = fullfile(theFiles(k).folder, baseFileName);

    % Reading the fragment
    I = imread(fullFileName);
    
    % Performing image segmentation via k-means of 2 
    [L,Centers] = imsegkmeans(I, 2);
    
    % Converting every value 2 to 255
    L(L==2)=255;
    
    % Converting grayscale image to binarized image 
    BW1 = im2bw(L,0.5);
    
    % Grabbing the largest object from image 
    BW2 = bwareafilt(BW1,1);
    
    % Filling holes in mask
    Mask = imfill(BW2,'holes');
    
    % Combining the mask and fragment
    Res = bsxfun(@times, I, cast(Mask, 'like', I));
    
    % Getting string value of k 
    % stringK = int2str(k);

    % Getting the dir to store the mask and fragment 
    position = find(theFiles(k).folder == '/', 1, 'last');
    newDir = extractAfter(theFiles(k).folder, position);
    
    % Dir for extracted mask 
    % Dir_frag = ['/data/p301438/IAAfragments_isolated_parchment_onlyColor-resized50/', newDir];
    Dir_frag = ['/projects/mdhali/BscProjects/Stephan/IAAfragments_isolated_parchment_onlyColor-resized50/', newDir];
    mkdir(Dir_frag)

    % Saving the 50 percent downscaled combination of fragment and mask 
    %imwrite(Res, ['/data/p301438/IAAfragments_isolated_parchment_onlyColor-resized50/', newDir ,'/', baseFileName]);
    imwrite(Res, ['/projects/mdhali/BscProjects/Stephan/IAAfragments_isolated_parchment_onlyColor-resized50/', newDir, '/', baseFileName]);
    
    % Dir for extracted mask ;
    % Dir_mask = ['/data/p301438/IAAfragments_parchment_mask_onlyColor-resized50/', newDir];
    Dir_mask = ['/projects/mdhali/BscProjects/Stephan/IAAfragments_parchment_mask_onlyColor-resized50/', newDir];
    mkdir(Dir_mask)
    
    % Saving the mask 
    % imwrite(Mask, ['/data/p301438/IAAfragments_parchment_mask_onlyColor-resized50/', newDir ,'/', baseFileName]);
    imwrite(Mask, ['/projects/mdhali/BscProjects/Stephan/IAAfragments_parchment_mask_onlyColor-resized50/', newDir, '/', baseFileName]);

end
