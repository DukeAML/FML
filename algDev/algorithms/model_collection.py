from algDev.algorithms.svm import SVM
from algDev.algorithms.cnn import CNN
from algDev.models.equity import Equity
from algDev.preprocessing import data_generator  
class ModelCollection:
    """a collection of models that each make a prediction for a given equity.
    
    Returns:
        ModelCollection -- object for storing and testing models
    """
    def __init__(self, ticker, type, features, params):
        """initialize model collection
        
        Arguments:
            ticker {string} -- security ticker
            type {string} -- type of all models (cnn, svm)
            features {string array} -- the features to be used in this collection
            params {dictionary} -- any extra parameters seen as useful, some examples
                                    include 
                                    length: the number of days in the input data,
                                    upper_threshold: documentation for label threshold,
                                    period: documentation for label period,
                                    cnn_split: number of cnns to use if necessary
        """
        self.eq = Equity(ticker)
        self.features = data_generator.parse_features(features)
        self.type = type
        self.params = params
        self.models = self.init_models()
        self.accuracy = 0.0
        
    def init_models(self):
        """Runs through all features and creates the appropriate models
        
        Returns:
            list -- list of models
        """
        models = []
        if self.type=='cnn':
            Xs, ys = data_generator.gen_cnn_data(self.eq, self.features, self.params['length'], self.params['upper_threshold'], self.params['period'], self.params['cnn_split'])
            for i in range(len(Xs)):
                models.append(CNN(Xs[i],ys[i], title=str(i)))
        elif self.type=='svm':
            for feature in self.features:
                X,y = data_generator.gen_svm_data(self.eq, [feature], self.params['length'], self.params['upper_threshold'], self.params['period'])
                print(len(X),len(y))
                models.append(SVM(X,y,title=feature))
        return models

    def update_params(self, params):
        """update the params field
        
        Arguments:
            params {dictionary} -- values to add or update to params
        """
        self.params.update(params)
    
    def add_params(self,params):
        """add to the params field
        
        Arguments:
            params {dictionary} -- values to add to params
        """
        self.update_params(params)

    def train_models(self):
        """Train all the models
        """
        for i, model in enumerate(self.models):
            model.train(self.params['data_splits'])
        self.update_accuracy()

    def update_accuracy(self):
        """Update the accuracy of the entire collection by averaging the
            individual accuracies, could probably be done better
        """
        acc = 0.0
        for model in self.models:
            acc += model.metrics['acc']

        self.accuracy = acc/len(self.accuracy)
        