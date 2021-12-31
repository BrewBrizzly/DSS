# Building a Siamese model 

from VGG16 import *
from utils import * 
import os 
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.metrics import Precision, Recall

# Function that connects two CNNS via a ECL layer
# which is connected to a block of dense layers 
def build_Siamese_network():

    # Configuring input layers for each sister
    Input_Image_A = Input(name = 'Image_A', shape = (256, 256, 3))
    Input_Image_B = Input(name = 'Image_B', shape = (256, 256, 3))

    # Defining the VGG16
    VGG16 = build_VGG16_network()

    # Connecting each image to VGG16
    VGG16_A = VGG16(Input_Image_A)
    VGG16_B = VGG16(Input_Image_B)

    # Connecting the each layer to lambda euclidian distance layer 
    distance = keras.layers.Lambda(euclidean_distance)([VGG16_A, VGG16_B])

    # Creating the final dense layers 
    x = keras.layers.Dense(512, activation="relu", name = 'block6_dense1')(distance)
    x = keras.layers.Dense(512, activation="relu", name = 'block6_dense2')(x)
    outputs = keras.layers.Dense(1, activation="sigmoid", name = 'block6_dense3')(x)

    # building the complete model 
    model = Model(inputs=[Input_Image_A, Input_Image_B], outputs=outputs, name = 'Siame_Network')	

    return model


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


# Building the left and right dataset
def build_data(Path_Positive_A, Path_Positive_B, Path_Negative_A, Path_Negative_B):

    # Getting the filenames for the positive pair, in same order 
    P_a = tf.data.Dataset.list_files(Path_Positive_A, shuffle = True, seed = 24)
    P_b = tf.data.Dataset.list_files(Path_Positive_B, shuffle = True, seed = 24)

    # Getting the directories for the negative pair, in same order 
    N_a = tf.data.Dataset.list_files(Path_Negative_A, shuffle = True, seed = 24)
    N_b = tf.data.Dataset.list_files(Path_Negative_B, shuffle = True, seed = 24)

    # Creating the positive pair
    P_pair = tf.data.Dataset.zip((P_a, P_b, tf.data.Dataset.from_tensor_slices(tf.ones(len(P_a)))))

    # Creating the negative pair 
    N_pair = tf.data.Dataset.zip((N_a, N_b, tf.data.Dataset.from_tensor_slices(tf.zeros(len(N_a)))))

    # Creating the overall dataset
    dataset = P_pair.concatenate(N_pair)

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

    return dataset


# From https://github.com/nicknochnack/FaceRecognition/blob/main/Facial%20Verification%20with%20a%20Siamese%20Network%20-%20Final.ipynb
@tf.function
def train_step(siamese_model, batch, binary_cross_loss, opt):
    
    # Record all of our operations 
    with tf.GradientTape() as tape:     
        # Get anchor and positive/negative image
        X = batch[:2]
        # Get label
        y = batch[2]
        
        # Forward pass
        yhat = siamese_model(X, training=True)
        # Calculate loss
        loss = binary_cross_loss(y, yhat)

    print(loss)
        
    # Calculate gradients
    grad = tape.gradient(loss, siamese_model.trainable_variables)
    
    # Calculate updated weights and apply to siamese model
    opt.apply_gradients(zip(grad, siamese_model.trainable_variables))
        
    # Return loss
    return loss


# From https://github.com/nicknochnack/FaceRecognition/blob/main/Facial%20Verification%20with%20a%20Siamese%20Network%20-%20Final.ipynb
def train(siamese_model, dataset, checkpoint, checkpoint_prefix, binary_cross_loss, opt, EPOCHS):
    # Loop through epochs
    for epoch in range(1, EPOCHS+1):
        print('\n Epoch {}/{}'.format(epoch, EPOCHS))
        progbar = tf.keras.utils.Progbar(len(dataset))
        
        # Creating a metric object 
        r = Recall()
        p = Precision()
        
        # Loop through each batch
        for idx, batch in enumerate(dataset):
            # Run train step here
            loss = train_step(siamese_model, batch, binary_cross_loss, opt)
            yhat = siamese_model.predict(batch[:2])
            r.update_state(batch[2], yhat)
            p.update_state(batch[2], yhat) 
            progbar.update(idx+1)
        print(loss.numpy(), r.result().numpy(), p.result().numpy())
        
        # Save checkpoints
        if epoch % 10 == 0: 
            checkpoint.save(file_prefix=checkpoint_prefix)
    
    # Save weights
    siamese_model.save('VGG16.h5')


# Builds the data and model to train it 
def run_model(A1, B1, A0, B0):

    # Settings for GPU, and a check
    phy_dev = tf.config.experimental.list_physical_devices('GPU')
    print("Num gpu: ", len(phy_dev))
    tf.config.experimental.set_memory_growth(phy_dev[0], True)

    # Getting the dataset into Tensorflow format 
    dataset = build_data(A1, B1, A0, B0)

    # Building the model with the dimensions of a patch
    siamese_model = build_Siamese_network()

    # Summary of the model as confirmation
    siamese_model.summary()

    # Below comes from: https://github.com/nicknochnack/FaceRecognition/blob/main/Facial%20Verification%20with%20a%20Siamese%20Network%20-%20Final.ipynb
    binary_cross_loss = tf.losses.BinaryCrossentropy()

    opt = tf.keras.optimizers.Adam(1e-4) # 0.0001

    checkpoint_dir = './training_checkpoints'
    checkpoint_prefix = os.path.join(checkpoint_dir, 'ckpt')
    checkpoint = tf.train.Checkpoint(opt=opt, siamese_model = siamese_model)

    train(siamese_model, dataset, checkpoint, checkpoint_prefix, binary_cross_loss, opt, 10)








