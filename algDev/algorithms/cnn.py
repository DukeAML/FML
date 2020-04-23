from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten
from keras.optimizers import SGD
from sklearn.utils import compute_class_weight
from keras.utils import to_categorical
import numpy as np
from algDev.preprocessing.data_generator import split_data
class CNN:
    """wrapper for a CNN model
    
    Returns:
        CNN -- model
    """
    def __init__(self, X, y, title='default'):
        """initialize CNN
        
        Arguments:
            X {ndarray} -- input data
            y {ndarray} -- labels
        
        Keyword Arguments:
            title {str} -- name of the model (default: {'default'})
        """
        self.data = {'features':X, 'labels':y}
        self.model = self.build_model(X.shape[1],X.shape[2])
        self.metrics = {}
        self.title = title
        
    def build_model(self):
        """Construct the CNN
        
        Returns:
            Sequential -- fully compiled model
            Model architecture (static for now): 
            Conv2D w/ 64 nodes -> Conv2D w/ 32 nodes -> Flatten -> Sigmoid
            Optimizer: SGD
        """
        #create model
        model = Sequential()
        #add model layers
        model.add(Conv2D(64, kernel_size=3, activation='relu', input_shape=(self.data['features'].shape[1],self.data['features'].shape[2],1)))
        model.add(Conv2D(32, kernel_size=3, activation='relu'))
        model.add(Flatten())
        model.add(Dense(1, activation='sigmoid'))
        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

        model.compile( loss = "categorical_crossentropy",   
               optimizer = sgd, 
               metrics=['accuracy']
             )
        return model

    def train(self, splits, X=None, y=None):
        """train the CNN
        
        Arguments:
            splits {int array} -- split of data between types
        
        Keyword Arguments:
            X {ndarray} -- train input data (default: {None})
            y {ndarray} -- train labels (default: {None})
        """
        if not X or not y:
            X = self.data['features']
            y = self.data['labels']
        
        X_train, y_train, X_val, y_val, X_test, y_test = split_data(X, y, splits)

        y_train = to_categorical(y_train)
        y_val = to_categorical(y_val) 
        y_test = to_categorical(y_test)
        
        self.model.fit(X_train, y_train, batch_size = 128, epochs = 200, verbose = 2, validation_data = (X_val, y_val))
        
        self.test(X_test, y_test)

    def test(self, X, y):
        """run a test over data points
        
        Arguments:
            X {ndarray} -- input data
            y {ndarray} -- labels
        """
        results = self.model.evaluate(X, y)
        
        self.metrics['acc'] = results['accuracy']

    def predict(self, Xi):
        """Make a prediction of a data point
        
        Arguments:
            Xi {ndarray} -- data point to predict on
        
        Returns:
            float -- prediction of the point
        """
        pred = self.model.predict(Xi)
        
        return pred