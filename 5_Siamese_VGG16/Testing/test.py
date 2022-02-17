# Measuring model performance 

# Required libraries
# from VGG16 import *
from utils import * 

# Required modules 
import numpy as np 
import tensorflow as tf 
from tensorflow import keras
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.metrics import Precision, Recall, Accuracy 

# Function that connects two CNNS via a eucledian distance layer
# which is connected to a block of dense layers, the output 
def build_Siamese_network():

    # Configuring the two input layers 
    Input_Image_A = Input(name = 'Image_A', shape = (256, 256, 3))
    Input_Image_B = Input(name = 'Image_B', shape = (256, 256, 3))

    # Defining the VGG16 
    VGG16 = build_VGG16_network()

    # Connecting input layer to a VGG16
    VGG16_A = VGG16(Input_Image_A)
    VGG16_B = VGG16(Input_Image_B)

    # Connecting each VGG16 to the lambda euclidian distance layer 
    distance = keras.layers.Lambda(euclidean_distance)([VGG16_A, VGG16_B])

    # Creating the final dense layers 
    x = keras.layers.Dense(512, activation = LeakyReLU(alpha=0.1), name = 'block6_dense1')(distance)
    x = keras.layers.Dense(512, activation = LeakyReLU(alpha=0.1), name = 'block6_dense2')(x)
    outputs = keras.layers.Dense(1, activation="sigmoid", name = 'block6_dense3')(x)

    # building the complete model 
    model = Model(inputs=[Input_Image_A, Input_Image_B], outputs=outputs, name = 'Siamese_Network')   

    return model

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

    return dataset


def test_model(path_model, A1, B1, A0, B0):

   # Settings for GPU, and a check if the gpu was detected 
    phy_dev = tf.config.experimental.list_physical_devices('GPU')
    
    print("Amount of GPU's: ", len(phy_dev))
    
    for gpu in phy_dev:
        tf.config.experimental.set_memory_growth(gpu, True)

    # Creating the testing dataset
    dataset = build_data(A1, B1, A0, B0)

    # Loading the trained model 
    model = tf.keras.models.load_model(path_model)
    # model = build_Siamese_network()
    # model.load_weights(checkpoint_filepath)

    # Summary of model as confirmation 
    model.summary()

    # Creating metric objects
    r = Recall()
    p = Precision()
    a = Accuracy()

    # Progress bar for testing 
    progbar = tf.keras.utils.Progbar(len(dataset))

    # Loop through each batch in the dataset 
    for idx, batch in enumerate(dataset):

        # Prediction with current batch 
        yhat = model.predict(batch[:2])

        # Processing the results to either 1 or 0
        yhat = [1 if value > 0.5 else 0 for value in yhat]

        # Update the metrics accordingly 
        r.update_state(batch[2], yhat)
        p.update_state(batch[2], yhat) 
        a.update_state(batch[2], yhat) 

        # Update the progress bar 
        progbar.update(idx + 1)
    
    # Calculate f measure 
    F = (2 * p.result().numpy() * r.result().numpy()) / (p.result().numpy() + r.result().numpy())

    # Storing the results in a list 
    test_ls = [r.result().numpy(), p.result().numpy(), a.result().numpy(), F]

    # Printing the metrics values after completing a single epoch     
    print(test_ls)

    # Saving the scores 
    np.save('test_results.npy', test_ls)
