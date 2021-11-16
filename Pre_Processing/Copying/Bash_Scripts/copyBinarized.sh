#!/bin/bash

source=/Users/stephannijdam/Desktop/Binarized/IAAfragments_onlyBinarized
dest=p301438@peregrine.hpc.rug.nl:/data/p301438/ 

rsync -avP $source $dest