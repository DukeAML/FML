import tensorflow as tf
from tensorflow import keras
from keras import models, layers
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Conv1D, LeakyReLU, BatchNormalization

print(tf.__version__)

# pull features, get train/test split
# choose batch size
# etc,

# B = batch_size
B = 30
# T = time_steps
T = 20


# build models 

# Generator = LSTM
def create_generator():
    model = Sequential()
    model.add(LSTM(128, dropout=.2))
    model.add(BatchNormalization())
    model.add(Dense(64, activation='relu'))
    model.add(Dense(1, activation="sigmoid"))

    return model


generator = create_generator()


# Discriminator = CNN
def create_discriminator():
    model = Sequential()

    # convolve, relu, drop
    model.add(Conv1D(64, 3, input_shape=(B, T, 25)))
    model.add(LeakyReLU())
    model.add(Dropout(0.2))

    model.add(Conv1D(128, 3))
    model.add(LeakyReLU())
    model.add(Dropout(0.2))

    model.add(Conv1D(220, 3))
    model.add(LeakyReLU())
    model.add(BatchNormalization())

    # flatten?
    model.add(Dense(1, activation="sigmoid"))

    return model


discriminator = create_discriminator()

# Define Loss Functions

cross_entropy = tf.keras.losses.BinaryCrossentropy()
