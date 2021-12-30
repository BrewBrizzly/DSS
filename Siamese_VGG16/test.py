# Test script to see if we can make a datastruct compatable for training 

import tensorflow as tf
from tensorflow import keras 
import numpy as np
from matplotlib import pyplot as plt 

# Getting the filenames for the positive pair, in same order 
P_a = tf.data.Dataset.list_files('/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15_exp/Training/Positive/A/*.jpg', shuffle = True, seed = 24)
P_b = tf.data.Dataset.list_files('/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15_exp/Training/Positive/B/*.jpg', shuffle = True, seed = 24)

# Getting the directories for the negative pair, in same order 
N_a = tf.data.Dataset.list_files('/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15_exp/Training/Negative/A/*.jpg', shuffle = True, seed = 24)
N_b = tf.data.Dataset.list_files('/projects/mdhali/BscProjects/Stephan/Model-Data/Cutoff_15_exp/Training/Negative/B/*.jpg', shuffle = True, seed = 24)

# Calculating the len of overall dataset
length = len(P_a) * 2 
length = length + (len(N_a) * 2)
print("Length is ", length)

# Creating the positive pair
P_pair = tf.data.Dataset.zip((P_a, P_b, tf.data.Dataset.from_tensor_slices(tf.ones(len(P_a)))))

# Creating the negative pair 
N_pair = tf.data.Dataset.zip((N_a, N_b, tf.data.Dataset.from_tensor_slices(tf.zeros(len(N_a)))))

# Creating the overall dataset
dataset = P_pair.concatenate(N_pair)

# Checking if everything is according desired format 
example = dataset.as_numpy_iterator() 

example = example.next()

print(example)


# Normalizing pixel values, no need for scaling 
def preprocess_img(path):

    # Read the image
    byte = tf.io.read_file(path)

    # Load the image 
    img = tf.io.decode_jpeg(byte)

    # Normalized image
    img = img / np.uint8(255.0)

    return img 

# Process the pairs 
def process_pairs(a, b, label):
    return (preprocess_img(a), preprocess_img(b), label)


# Processing the dataset
dataset = dataset.map(process_pairs)

# Caching for performance 
dataset = dataset.cache()

# Shuffling for performance in training
dataset = dataset.shuffle(buffer_size = 1024)

# Batching the dataset for prefenting bottleneck 
dataset = dataset.batch(16) 

# Prefetching for performance 
dataset = dataset.prefetch(8)

# Showing a pair 
dataset = dataset.as_numpy_iterator()
dataset = dataset.next()
print(dataset)
print(len(dataset))
print(len(dataset[0]))
print(dataset[2])
plt.imshow(dataset[0])




















