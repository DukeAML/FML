from tensorflow import keras
from keras.models import Sequential
from keras.layers import BatchNormalization, LeakyReLU, LSTM, Dense, Dropout, Flatten, Input, concatenate
from keras.utils import plot_model
from gen_lstm_data import gen_data, gen_labels, get_data_labelled
import numpy as np

# input should be [batch_size, time_steps, features] = [30, 19, 25]
# labels = 10 classes


(X_train, y_train, X_test, y_test) = gen_data(eq = "VSLR", verbose= True)

model1a.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy', 'mae', 'mse'])
model1a.fit(X_train, y_train, batch_size=32, epochs=500, verbose=2, validation_split=.2)
predictions = np.array(model1a.predict(X_test))
X_test_arr = np.array(X_test)
y_test_arr = np.array(y_test)
np.savetxt('features.csv', X_test_arr[0], delimiter=',')
np.savetxt('predictions.csv', predictions[0], delimiter=',')
np.savetxt('actual.csv', y_test_arr[0], delimiter=',')
score = model1a.evaluate(X_test, y_test, batch_size=32, verbose=2)
print(score)

