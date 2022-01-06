# Measuring model performance 

# Required modules 
import numpy as np 
import tensorflow as tf 
from tensorflow.keras.metrics import Precision, Recall, Accuracy


# Normalizing pixel values of the data, no need for scaling 
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

# Building the left and right dataset
def build_data(Path_Positive_A, Path_Positive_B, Path_Negative_A, Path_Negative_B):

    # Getting the filenames for the positive pair, in same order by setting the seed 
    P_a = tf.data.Dataset.list_files(Path_Positive_A, shuffle = True, seed = 24)
    P_b = tf.data.Dataset.list_files(Path_Positive_B, shuffle = True, seed = 24)

    # Getting the filenames for the negative pair, in same order by setting the seed 
    N_a = tf.data.Dataset.list_files(Path_Negative_A, shuffle = True, seed = 24)
    N_b = tf.data.Dataset.list_files(Path_Negative_B, shuffle = True, seed = 24)

    # Creating the positive pair
    P_pair = tf.data.Dataset.zip((P_a, P_b, tf.data.Dataset.from_tensor_slices(tf.ones(len(P_a)))))

    # Creating the negative pair 
    N_pair = tf.data.Dataset.zip((N_a, N_b, tf.data.Dataset.from_tensor_slices(tf.zeros(len(N_a)))))

    # Creating the overall dataset
    dataset = P_pair.concatenate(N_pair)

    # Calculating the buffer size 
    buffer_size = len(N_a) * 2

    # Shuffling the dataset 
    dataset = dataset.shuffle(buffer_size = buffer_size)

    # Processing the dataset
    dataset = dataset.map(process_pairs)

    # Batching the dataset for prefenting bottleneck, size according paper
    dataset = dataset.batch(16) 

    # Prefetching for performance 
    dataset = dataset.prefetch(8)

    return dataset, buffer_size


def test_model(path_model, A1, B1, A0, B0):

    # Settings for GPU, and a check if the gpu was detected 
    phy_dev = tf.config.experimental.list_physical_devices('GPU')
    print("Num gpu: ", len(phy_dev))
    tf.config.experimental.set_memory_growth(phy_dev[0], True)

    # Creating the testing dataset
    dataset = build_data(A1, B1, A0, B0)

    # Loading the trained model 
    model = tf.keras.models.load_model(path_model)

    # Summary of model as confirmation 
    model.summary()

    print('Finished')


