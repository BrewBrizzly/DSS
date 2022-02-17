# Determines the most representative patch of a fragment
# On the basis of the amount of non-black pixels

# Required modules
import cv2

def det_represent(fragment):

    # Patch with lowest amount of black pixels
    max_value = 0

    # looping through patches in fragment
    for patch in fragment:

        # Load the patch as grayscale
        patch_img = cv2.imread(patch, 0)

        # Count of non black pixels
        cnt = cv2.countNonZero(patch_img)

        # Check if amount of non black pixels is higher than the current highest
        if cnt > max_value:

            repr_patch = patch
            max_value = cnt

    return [repr_patch]

