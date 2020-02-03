import tensorflow as tf
from tensorflow.keras import layers, models
from gensim.models import KeyedVectors

# second model (w/ text)
model_inputNum = layers.Input(shape=(19, 125))  # assuming we have 125 numerical features per time-step
model_inputText = layers.Input(shape=(19, 200))  # assuming we have 200 words per time-step

# for numerics
LSTM = layers.LSTM(125, dropout=.2)(model_inputNum)
Batch_Norm = layers.BatchNormalization()(LSTM)

# for text

# wvmodel = shorttext.utils.load_word2vec_model('/Users/phoebeloveklett/Downloads/GoogleNews-vectors-negative300.bin.gz')
wvmodel = KeyedVectors.load_word2vec_format('/Users/phoebeloveklett/Downloads/GoogleNews-vectors-negative300.bin.gz',
                                            binary=True)
# index all input text
word_vectors = wvmodel.wv
Embed = (word_vectors) * (model_inputText)  # this is wrong fix this
Drop = layers.Dropout(.2)(Embed)

# concatenate numerical, text inputs
Concat = layers.concat([Drop, Batch_Norm], axis=0)

Dense1 = layers.Dense(64)(Concat)
LR = layers.LeakyRelu()(Dense1)
Drop = layers.Dropout(.2)(Dense1)
Dense2 = layers.Dense(28, activation='relu')(Drop)
model_output = layers.Dense(10, activation="softmax")(Dense2)  # use softmax if not binary, sigmoid otherwise

model2 = tf.keras.Model([model_inputNum, model_inputText], model_output)
model2.summary()
