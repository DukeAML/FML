from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
from tensorflow import keras 
from tensorflow.keras import layers,models
from keras.utils.vis_utils import model_to_dot
from gensim.models import KeyedVectors
# from gensim.models.word2vec import Word2Vec
# import gensim.downloader as api

# import shorttext

#create model to reduce dimensionality: LSTM -> Dense + Regularization
#input should be [batch_size, time_steps, features]
#labels = ??

model_inputNum = layers.Input(shape = (19,125)) #assuming we have 125 numerical features per time-step
model_inputText = layers.Input(shape = (19,200)) #assuming we have 200 words per time-step

#for numerics
LSTM =  layers.LSTM(125, dropout = .2)(model_inputNum)
Batch_Norm = layers.BatchNormalization()(LSTM)

#for text

#wvmodel = shorttext.utils.load_word2vec_model('/Users/phoebeloveklett/Downloads/GoogleNews-vectors-negative300.bin.gz')
wvmodel = KeyedVectors.load_word2vec_format('/Users/phoebeloveklett/Downloads/GoogleNews-vectors-negative300.bin.gz', binary=True)

# api.load("GoogleNews-vectors-negative300.bin")
# model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
#model = KeyedVectors.load_word2vec_format('./model/GoogleNews-vectors-negative300.bin', binary=True)(model_inputText)  
#Embed = api.load("word2vec-google-news-300")
Drop = layers.Dropout(.2)(wvmodel)

#concatenate numerical, text inputs 
Concat = layers.concat([Drop, Batch_Norm], axis =0)

Dense1 = layers.Dense(64)(Concat)
LR = layers.LeakyRelu()(Dense1)
Drop = layers.Dropout(.2)(Dense1)
Dense2 = layers.Dense(28, activation = 'relu')(Drop)
model_output = layers.Dense(1, activation = "sigmoid")(Dense2) #use softmax if not binary, sigmoid otherwise 

model = tf.keras.Model([model_inputNum, model_inputText], model_output)
model.summary()

keras.utils.plot_model(model, 'my_first_model.png')

