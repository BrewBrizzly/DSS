# Building a Siamese model 

from VGG16 import *
from utils import * 
import os 
import numpy as np
import tensorflow as tf
from tensorflow import keras
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
    x = keras.layers.Dense(512, activation="relu", name = 'block6_dense1')(distance)
    x = keras.layers.Dense(512, activation="relu", name = 'block6_dense2')(x)
    outputs = keras.layers.Dense(1, activation="sigmoid", name = 'block6_dense3')(x)

    # building the complete model 
    model = Model(inputs=[Input_Image_A, Input_Image_B], outputs=outputs, name = 'Siame_Network')	

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

    # Shuffling for performance in training
    b_size =  len(N_a) * 2
    print("The complete size of the dataset is: ", b_size)
    dataset = dataset.shuffle(buffer_size = b_size)

    # Processing the dataset
    dataset = dataset.map(process_pairs)

    # Batching the dataset for prefenting bottleneck, size according paper
    dataset = dataset.batch(16) 

    # Prefetching for performance 
    dataset = dataset.prefetch(8)

    return dataset


# From https://github.com/nicknochnack/FaceRecognition/blob/main/Facial%20Verification%20with%20a%20Siamese%20Network%20-%20Final.ipynb
# Performs one training step of the model during an epoch 
@tf.function
def train_step(siamese_model, batch, binary_cross_loss, opt):
    
    # Record all of our operations 
    with tf.GradientTape() as tape:    

        # Getting one pair out of the batch, current implementation might be wrong 
        X = batch[:2]

        # Getting the label of the pair 
        y = batch[2]
        
        # A single forward pass with a pair 
        yhat = siamese_model(X, training=True)

        # Calculate loss with the label and the predicted outcome 
        loss = binary_cross_loss(y, yhat)
        
    # Calculate the gradients that need to be applied to the model 
    grad = tape.gradient(loss, siamese_model.trainable_variables)
    
    # Applying the gradients to the model 
    opt.apply_gradients(zip(grad, siamese_model.trainable_variables))
        
    # Return the current loss value
    return loss


# From https://github.com/nicknochnack/FaceRecognition/blob/main/Facial%20Verification%20with%20a%20Siamese%20Network%20-%20Final.ipynb
# Training loop that goes through all the epochs set
def train(siamese_model, dataset, checkpoint, checkpoint_prefix, binary_cross_loss, opt, EPOCHS):

    # List to keep track of loss over epochs 
    ls_loss = [] 

    # Setting the patience for the early stop
    patience = 3 

    # Loop through each epoch
    for epoch in range(1, EPOCHS + 1):

    	# Printing the current status 
        print('\n Epoch {}/{}'.format(epoch, EPOCHS))
        progbar = tf.keras.utils.Progbar(len(dataset))
        
        # Creating metric objects
        r = Recall()
        p = Precision()
        a = Accuracy()
        
        # Loop through each batch in the dataset 
        for idx, batch in enumerate(dataset):

            # Single training step
            loss = train_step(siamese_model, batch, binary_cross_loss, opt)

            # Prediction with current batch 
            yhat = siamese_model.predict(batch[:2])

            # Update the metrics accordingly 
            r.update_state(batch[2], yhat)
            p.update_state(batch[2], yhat) 
            a.update_state(batch[2], yhat)

            # Update the progress bar 
            progbar.update(idx + 1)

        # Printing the metrics values after completing a single epoch     
        print(loss.numpy(), r.result().numpy(), p.result().numpy(), a.result().numpy())

        # Append the loss 
        ls_loss.append(loss.numpy())

        # Save weights each time 10 epochs have passed
        if epoch % 10 == 0: 
            checkpoint.save(file_prefix = checkpoint_prefix)

        # If model is not improving then break 
        if len(ls_loss) > patience: 
            if ls_loss[-1] >= ls_loss[-patience]:
                break
    

    # Save weights after having completed training 
    siamese_model.save('VGG16.h5')

    # Saving the losses 
    np.save('VGG16_losses.npy', ls_loss)


# Builds the data and model to train it 
def run_model(A1, B1, A0, B0):

    # Settings for GPU, and a check if the gpu was detected 
    phy_dev = tf.config.experimental.list_physical_devices('GPU')
    print("Num gpu: ", len(phy_dev))
    tf.config.experimental.set_memory_growth(phy_dev[0], True)

    # Preprocessing the data before passing to model 
    dataset = build_data(A1, B1, A0, B0)

    # Building the model with the dimensions according the dataset
    siamese_model = build_Siamese_network()

    # Summary of the model as confirmation
    siamese_model.summary()

    # Below comes from: https://github.com/nicknochnack/FaceRecognition/blob/main/Facial%20Verification%20with%20a%20Siamese%20Network%20-%20Final.ipynb

    # Initializing the loss function
    binary_cross_loss = tf.losses.BinaryCrossentropy()

    # Initializing the model's optimizer according to the value found in the paper 
    opt = tf.keras.optimizers.Adam(0.001) 

    checkpoint_dir = './training_checkpoints'
    checkpoint_prefix = os.path.join(checkpoint_dir, 'ckpt')
    checkpoint = tf.train.Checkpoint(opt = opt, siamese_model = siamese_model)

    train(siamese_model, dataset, checkpoint, checkpoint_prefix, binary_cross_loss, opt, 5)








