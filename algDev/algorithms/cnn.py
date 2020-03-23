from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten
from gen_picture_data import gen_data

X, y = gen_data('AAPL')

print(X.shape)
print(y.shape)

n = len(X)
t_size = int(n * .8)

X_train = X[50:t_size,:]
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], X_train.shape[2], 1)
print(X_train.shape)
X_test = X[t_size:len(X),:]
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], X_test.shape[2], 1)
print(X_test.shape)
y_train = y[(-1 * (n-50)):(-1 * (n-t_size))]
print(y_train.shape)
y_test = y[(-1 * (n-t_size)):len(y)]
print(y_test.shape)
#create model
model = Sequential()
#add model layers
model.add(Conv2D(64, kernel_size=3, activation='relu', input_shape=(25,25,1)))
model.add(Conv2D(32, kernel_size=3, activation='relu'))
model.add(Flatten())
model.add(Dense(1, activation='softmax'))
#compile model using accuracy to measure model performance
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

#train the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=500)