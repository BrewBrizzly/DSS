#!/bin/bash

source=/projects/mdhali2/DssProject/data/IAAfragments
dest=/projects/mdhali2/BScProjects21/Stephan/Fragments/RGB/

for d in $source/*; do
	rsync -avnP $d/fragments/*.tif $dest
done
 
