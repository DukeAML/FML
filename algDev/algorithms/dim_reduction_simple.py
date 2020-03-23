from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
from tensorflow import keras 
from tensorflow.keras import layers,models
from keras.utils.vis_utils import model_to_dot

#create model to reduce dimensionality: LSTM -> Dense + Regularization
#input should be [batch_size, time_steps, features]
#labels = ??

model_input = layers.Input(shape = (19,125))
LSTM =  layers.LSTM(125, dropout = .2)(model_input)
Batch_Norm = layers.BatchNormalization()(LSTM)
Dense1 = layers.Dense(64, activation = 'relu')(Batch_Norm)
Drop = layers.Dropout(.2)(Dense1)
Dense2 = layers.Dense(28, activation = 'relu')(Drop)
model_output = layers.Dense(1, activation = "softmax")(Dense2) #use softmax if not binary, sigmoid otherwise 

model = tf.keras.Model(model_input, model_output)
model.summary()

keras.utils.plot_model(model, 'my_first_model.png')

