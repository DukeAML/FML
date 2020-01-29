# from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
from tensorflow import keras 
from keras.models import Sequential
from keras.layers import *
from keras.utils import plot_model


#input should be [batch_size, time_steps, features]
#labels = 10 classes


#first model (w/o text pipeline)
def create_model1a():
    model = Sequential()
    model.add(LSTM(125,  dropout = .2, input_shape= (20,25) ))
    model.add(BatchNormalization())
    model.add(Dense(64))
    model.add(LeakyReLU())
    model.add(Dropout(.2))
    model.add(Dense(28))
    model.add(LeakyReLU())
    model.add(BatchNormalization())
    model.add(Dense(10, activation = "softmax"))
    return model

model1a = create_model1a()

def create_model1b():
    model = Sequential()
    model.add(LSTM(125,  dropout = .2, return_sequences=True, input_shape= (20,25)))
    model.add(LSTM(125,  dropout = .2, return_sequences=True))
    model.add(LSTM(125,  dropout = .2, return_sequences=False))
    model.add(BatchNormalization())
    model.add(Dense(64))
    model.add(LeakyReLU())
    model.add(Dropout(.2))
    model.add(BatchNormalization())
    model.add(Dense(10, activation = "softmax"))
    return model

model1b = create_model1b()

# plot_model(model1b, to_file='model1b.png')

model1a.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
print("model compiled")

# model.fit(x_train, y_train, batch_size=64, epochs=5, validation_data=(x_val, y_val))



