from sklearn import svm
from build_dfFeatures import gen_features
from gen_indicators import gen_data
from svm import svm_collection
from models.equity import Equity

class Voter:
    """Voting algorithm class
    
    Returns:
        Voter -- Object for running votes
    """
    self.valid_voting_types = [
        'accuracy'
    ]
    def __init__(self, voting_type):
        """initialize voter
        
        Arguments:
            voting_type {string} -- the voting mechanism to use (see docs)
        """
        super().__init__()
        assert voting_type in self.valid_voting_types
        self.voting_type = voting_type
        
    def predict(self, model_collection, data):
        """make a prediction of the data for a given model_collection
        
        Arguments:
            model_collection {ModelCollection} -- Object to predict with
            data {ndarray} -- set of data to make predict of
        
        Returns:
            (int, float) -- predicted class and models accuracy in tuple
        """
        predictions = {}
        for model in model_collection.models:
            prediction = model.predict(data)
            predictions[model.title] = (prediction, model.metrics['acc'])
        
        if self.voting_type == "accuracy":

            sum_voting = 0
            for pred in predictions.items():
                sum_voting += pred[0]*pred[1]
                sum_voting += pred[0]*pred[1]

            if sum_voting > 4:
                prediction = [1]

            else:
                prediction = [0]

        else:
            prediction = 'you have not selected a valid voting method'

        return (prediction, model_collection.accuracy)
