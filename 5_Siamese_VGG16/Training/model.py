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

    # Calculating the full dataset size 
    size_data = len(N_a) * 2

    # Splitting the data into training and validation 
    training_size = int(0.8 * size_data) 
    validation_size = size_data - training_size

    # Creating the train and validation dataset
    training_set = dataset.take(training_size)
    validation_set = dataset.skip(training_size)

    # Calculating the full dataset size 
    size_data = len(N_a) * 2

    return training_set, validation_set, training_size, validation_size


# Loading, preprocessing and shuffling the training dataset
def load_training(dataset, buffer_size):

    print("The complete size of the training set is: ", buffer_size)
    dataset = dataset.shuffle(buffer_size = buffer_size)

    # Processing the dataset
    dataset = dataset.map(process_pairs)

    # Batching the dataset for prefenting bottleneck, size according paper
    dataset = dataset.batch(16) 

    # Prefetching for performance 
    dataset = dataset.prefetch(8)

    return dataset

# Loading, preprocessing and shuffling the validation dataset
def load_validation(dataset, buffer_size):

    print("The complete size of the validation set is: ", buffer_size)
    dataset = dataset.shuffle(buffer_size = buffer_size)

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
def train(siamese_model, training, testing, checkpoint, checkpoint_prefix, binary_cross_loss, opt, buffer_size_training, buffer_size_validating, EPOCHS):

    # List to keep track of performance over training epochs 
    performance_t = [] 

    # List to keep track of performance over validation epochs 
    performance_v = [] 

    # Loading validation set
    loaded_validation = load_validation(testing, buffer_size_validating)

    # Setting the patience for the early stop
    # patience = 10

    # Loop through each epoch
    for epoch in range(1, EPOCHS + 1):

        # Loading, preprocessing and shuffling the dataset
        loaded_training = load_training(training, buffer_size_training)

    	# Printing the current status 
        print('\n Epoch {}/{}'.format(epoch, EPOCHS))
        progbar = tf.keras.utils.Progbar(len(loaded_training))
        
        # Creating metric objects for training
        rt = Recall()
        pt = Precision()
        at = Accuracy()

        # Creating the metric object for validation
        rv = Recall()
        pv = Precision()
        av = Accuracy

        # Loop through each batch in the training set, updating the weights  
        for idx, batch in enumerate(loaded_training):

            # Single training step
            loss = train_step(siamese_model, batch, binary_cross_loss, opt)

            # Prediction with current batch 
            yhat = siamese_model.predict(batch[:2])

            # Processing the results to either 1 or 0
            [1 if value > 0.5 else 0 for value in yhat]

            # Update the metrics accordingly 
            rt.update_state(batch[2], yhat)
            pt.update_state(batch[2], yhat) 
            at.update_state(batch[2], yhat) 

            # Update the progress bar 
            progbar.update(idx + 1)

        # Printing the metrics values after completing a single epoch of training    
        print('Training loss: ', loss.numpy(), ' recall: ', rt.result().numpy(), ' precision: ', pt.result().numpy(), ' accuracy: ', at.results.numpy())

        # Append the training values to array
        performance_t.append([loss.numpy(), rt.result().numpy(), pt.result().numpy(), at.results.numpy()])

        print("\n Validating the network")
        progbar = tf.keras.utils.Progbar(len(loaded_validation))

        # Loop through each batch in the validation set  
        for idx, batch in enumerate(loaded_validation):

            # Prediction with current validation batch 
            yhat = siamese_model.predict(batch[:2])

            # Processing the results to either 1 or 0
            [1 if value > 0.5 else 0 for value in yhat]

            # Calculate loss with the label and the predicted outcome 
            loss = binary_cross_loss(batch[2], yhat)

            # Updating the metrics
            rv.update_state(batch[2], yhat)
            pv.update_state(batch[2], yhat) 
            av.update_state(batch[2], yhat) 

            # Update the progress bar 
            progbar.update(idx + 1)
        
        # Printing the metrics values after completing a single epoch of validating    
        print('Validation loss: ', loss.numpy(), ' recall: ', rv.result().numpy(), ' precision: ', pv.result().numpy(), ' accuracy: ', av.results.numpy())

        # Append the training values to array
        performance_v.append([loss.numpy(), rv.result().numpy(), pv.result().numpy(), av.results.numpy()])


        # Save weights each time 10 epochs have passed
        if epoch % 5 == 0: 
            checkpoint.save(file_prefix = checkpoint_prefix)

        # If model is not improving then break 
        # if len(ls_loss) > patience: 
        #     if ls_loss[-1] >= ls_loss[-patience]:
        #         break

    # Save weights after having completed training 
    siamese_model.save('VGG16.h5')

    # Saving the performance of training and validation
    np.save('VGG16_training.npy', performance_t, allow_pickle = True)
    np.save('VGG16_validation.npy', performance_v, allow_pickle = True)


# Builds the data and model to train it 
def run_model(A1, B1, A0, B0):

    # Settings for GPU, and a check if the gpu was detected 
    phy_dev = tf.config.experimental.list_physical_devices('GPU')
    print("Num gpu: ", len(phy_dev))
    tf.config.experimental.set_memory_growth(phy_dev[0], True)

    # Building the training set and the validation set
    training, testing, buffer_size_training, buffer_size_validating = build_data(A1, B1, A0, B0)

    # Building the model with the dimensions according the dataset
    siamese_model = build_Siamese_network()

    # Summary of the model as confirmation
    siamese_model.summary()

    # Below comes from: https://github.com/nicknochnack/FaceRecognition/blob/main/Facial%20Verification%20with%20a%20Siamese%20Network%20-%20Final.ipynb

    # Initializing the loss function
    binary_cross_loss = tf.losses.BinaryCrossentropy()

    # Initializing the model's optimizer according to the value found in the paper 
    opt = tf.keras.optimizers.Adam(0.0001) 

    checkpoint_dir = './training_checkpoints'
    checkpoint_prefix = os.path.join(checkpoint_dir, 'ckpt')
    checkpoint = tf.train.Checkpoint(opt = opt, siamese_model = siamese_model)

    train(siamese_model, training, testing, checkpoint, checkpoint_prefix, binary_cross_loss, opt, buffer_size_training, buffer_size_validating, 100)








