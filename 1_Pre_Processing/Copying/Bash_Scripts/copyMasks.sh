#!/bin/bash

source=/projects/mdhali2/DssProject/data/IAAfragments
dest=/mnt/data/

for d in $source/*; do
	rsync -avnP $d/fragments/*.tif $dest
done
 
