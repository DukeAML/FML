from tensorflow import keras
from keras.models import Sequential
# import pydot
# from gensim.models import KeyedVectors
from keras.layers import BatchNormalization, LeakyReLU, LSTM, Dense, Dropout, Flatten, Input, concatenate
from keras.utils import plot_model
from gen_lstm_data import gen_data, gen_labels, get_data_labelled
import numpy as np

# input should be [batch_size, time_steps, features] = [30, 19, 25]
# labels = 10 classes


(X_train, y_train, X_test, y_test) = gen_data(eq = "AAPL", verbose= True)
print(y_train[0])
print(X_train[0])


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
    model.add(Dense(25, activation = "softmax")) 
    return model


model1a = create_model1a()
# keras.utils.plot_model(model1a, 'my_first_model.png')


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
model1a.fit(X_train, y_train, batch_size=32, epochs=500, verbose=2, validation_split=.2)
score = model1a.evaluate(X_test, y_test, batch_size=32, verbose=2)
print(score)



