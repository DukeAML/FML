import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from gensim.models import KeyedVectors
from keras.layers import BatchNormalization, LeakyReLU, LSTM, Dense, Dropout, Flatten, Input, Concatenate
from keras.utils import plot_model
from gen_lstm_data import gen_data, gen_labels, get_data_labelled
import numpy as np

# input should be [batch_size, time_steps, features] = [30, 19, 25]
# labels = 10 classes

#input should be [batch_size, time_steps, features] = [30, 19, 25]
#labels = 10 classes

(X_train, y_train, X_test, y_test) = gen_data(eq = "VSLR", verbose= True)
print(y_train[0].shape)
print(X_train[0].shape)


# first model (w/o text pipeline)
def create_model1a():
    model = Sequential()
    model.add(LSTM(125, dropout=.2, input_shape=(19, 25)))
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
    model.add(LSTM(125, dropout=.2, return_sequences=True, input_shape=(19, 25)))
    model.add(LSTM(125, dropout=.2, return_sequences=True))
    model.add(LSTM(125, dropout=.2, return_sequences=False))
    model.add(BatchNormalization())
    model.add(Dense(64))
    model.add(LeakyReLU())
    model.add(Dropout(.2))
    model.add(BatchNormalization())
    model.add(Dense(10, activation="softmax"))
    return model


model1b = create_model1b()

# plot_model(model1b, to_file='model1b.png')

model1a.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy', 'mae', 'mse'])
model1a.fit(X_train, y_train, batch_size=30, epochs=500, verbose=2, validation_split=.2)
score = model1a.evaluate(X_test, y_test, batch_size=30, verbose=2)
print(score)

# model1b.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy', 'mae', 'mse'])
# model1b.fit(X_train, y_train, batch_size=30, epochs=500, verbose= 2, validation_split= .2)
# score = model1b.evaluate(X_test, y_test, batch_size=30, verbose=2)
# print(score)

# we want labels to look like [batch, 19, 1]


# from gensim.models.word2vec import Word2Vec
# import gensim.downloader as api

# import shorttext

# create model to reduce dimensionality: LSTM -> Dense + Regularization
# input should be [batch_size, time_steps, features]
# labels = ??

model_inputNum = Input(shape=(19, 125))  # assuming we have 125 numerical features per time-step
model_inputText = Input(shape=(19, 200))  # assuming we have 200 words per time-step

# for numerics
LSTM = LSTM(125, dropout=.2)(model_inputNum)
Batch_Norm = BatchNormalization()(LSTM)

# for text

# wvmodel = shorttext.utils.load_word2vec_model('/Users/phoebeloveklett/Downloads/GoogleNews-vectors-negative300.bin.gz')
wvmodel = KeyedVectors.load_word2vec_format('/Users/phoebeloveklett/Downloads/GoogleNews-vectors-negative300.bin.gz',
                                            binary=True)

# api.load("GoogleNews-vectors-negative300.bin")
# model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
# model = KeyedVectors.load_word2vec_format('./model/GoogleNews-vectors-negative300.bin', binary=True)(model_inputText)
# Embed = api.load("word2vec-google-news-300")
Drop = Dropout(.2)(wvmodel)

# concatenate numerical, text inputs
Concat = Concatenate([Drop, Batch_Norm], axis=0)

Dense1 = Dense(64)(Concat)
LR = LeakyReLU()(Dense1)
Drop = Dropout(.2)(Dense1)
Dense2 = Dense(28, activation='relu')(Drop)
model_output = Dense(1, activation="sigmoid")(Dense2)  # use softmax if not binary, sigmoid otherwise

model = tf.keras.Model([model_inputNum, model_inputText], model_output)
model.summary()

keras.utils.plot_model(model, 'my_first_model.png')
