from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten
from keras.optimizers import SGD
from sklearn.utils import compute_class_weight
from keras.utils import to_categorical
import numpy as np
class CNN:
    def __init__(self, shape):
        self.model = self.build_model(shape[1],shape[2])

        
    def build_model(self, input_width, input_height):

        #create model
        model = Sequential()
        #add model layers
        model.add(Conv2D(64, kernel_size=3, activation='relu', input_shape=(input_width,input_height,1)))
        model.add(Conv2D(32, kernel_size=3, activation='relu'))
        model.add(Flatten())
        model.add(Dense(1, activation='sigmoid'))
        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

        model.compile( loss = "categorical_crossentropy",   
               optimizer = sgd, 
               metrics=['accuracy']
             )
        return model

    def train_model(self,X_train,y_train, X_val, y_val):
        
        y_train = to_categorical(y_train)
        y_val = to_categorical(y_val) 
        # classWeight = compute_class_weight('balanced', np.unique(y_train), np.asarray(y_train)) 
        # classWeight = dict(enumerate(classWeight))
        self.model.fit(X_train, y_train, batch_size = 128, epochs = 200, verbose = 2, validation_data = (X_val, y_val))
        
        