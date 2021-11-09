% Specify the folder where the files live.
myFolder = '/data/p301438/IAAfragments_onlyColor-resized50';

% File pattern, in this case .jpg
filePattern = fullfile(myFolder, '**/*.jpg');

% List of all the names of the files that match pattern
theFiles = dir(filePattern);

for k = 1 : length(theFiles)

    % Determine the path to the file 
    baseFileName = theFiles(k).name;
    fullFileName = fullfile(theFiles(k).folder, baseFileName);

    % Reading the fragment
    I = imread(fullFileName);
    
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
    
    % Getting string value of k 
    stringK = int2str(k);

    % Getting the dir to store the mask and fragment 
    position = find(theFiles(k).folder == '/', 1, 'last');
    newDir = extractAfter(theFiles(k).folder, position);

    % Saving the 50 percent downscaled combination of fragment and mask 
    imwrite(Res, ['/data/p301438/IAAfragments_parchment_onlyColor-resized50/', newDir ,'/', baseFileName]);
    
    % Saving the mask 
    imwrite(Mask, ['/data/p301438/IAAfragments_parchment_mask_onlyColor-resized50/', newDir ,'/', baseFileName]);

end
