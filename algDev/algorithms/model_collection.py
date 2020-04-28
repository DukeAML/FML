from algDev.algorithms.svm import SVM
from algDev.algorithms.cnn import CNN
from algDev.models.equity import Equity
from algDev.preprocessing import data_generator  

class ModelCollection:
    """a collection of models that each make a prediction for a given equity.
    
    Returns:
        ModelCollection -- object for storing and testing models
    """
    def __init__(self, ticker, type, features=[], params=None, models=[], model_params =None):
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
            models {list} -- any pretrained models to import
            model_params {dictionary} -- model parameters to use (gamma, C) for all individual models
        """
        self.eq = Equity(ticker)
        self.ticker = ticker
        self.features = data_generator.parse_features(features)
        self.type = type
        self.params = params
        if 'data_splits' not in self.params:
            self.add_params({'data_splits': [0.8,0.2]})
        
        self.model_params = model_params
        if len(models) > 0:
            self.models = models
            self.update_accuracy()
        else:
            assert(len(features)>0)
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
                
                models.append(SVM(X,y,title=feature, params= self.model_params,metrics={}))

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

    def train_models(self, verbose=False):
        """Train all the models
        """
        if verbose:
            print("Training Models for ", self.eq.ticker)
        for i, model in enumerate(self.models):
            model.train(self.params['data_splits'], verbose = verbose)
            
        self.update_accuracy()

    def plot_rocs(self, verbose=False):
        """ Plot roc curve for each model
        """
        for model in self.models:
            model.plot_roc(verbose)

    def get_conf_matricies(self, verbose=False):
        """ returns confusion matrices for each model
        """
        cm_list =[]
        for model in self.models:
            cm = model.build_conf_matrix(self.params['data_splits'])
            cm_list.append(cm)

        return cm_list

    def get_voter_metrics(self, verbose=False):
        """ calculates metrics for voter 
        """
        for model in self.models:
            splits= self.params['data_splits']
            model.voter_metrics(splits, verbose)
        
        

        
    def update_accuracy(self):
        """Update the accuracy of the entire collection by averaging the
            individual accuracies, could probably be done better
        """
        acc = 0.0
        for model in self.models:

            print("Model ", model.title, " acc ", model.metrics['acc'])
            acc += model.metrics['acc']
        
        self.accuracy = acc/len(self.models)


    def predict(self, date, verbose=False):
        """ generate predictions for given date
        """
        if verbose:
            print(date)
        start_index = self.eq.get_index_from_date(date)
        end_index = start_index + self.params['length']
        
        predictions = []
        if self.type=='cnn':
            X_i = data_generator.get_subset(self.eq, self.features, start_index, end_index, self.type)
            for model in self.models:
                predictions.append(model.predict(X_i))
        elif self.type=='svm':
            for i,f in enumerate(self.features):
                X_i = data_generator.get_subset(self.eq, [f], start_index, end_index, self.type)
                predictions.append(self.models[i].predict(X_i))
        print("Todays Features: ", X_i)
        return predictions

    def grid_search_coll(self, verbose=False):
        ''' do grid search on model parameters gamma, C for each model
        '''
        for model in self.models:
            model.grid_search_model(verbose)


    