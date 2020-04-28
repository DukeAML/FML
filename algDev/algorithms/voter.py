from sklearn import svm
from algDev.algorithms.svm import SVM
from algDev.models.equity import Equity
import math

class Voter:
    """Voting algorithm class
    
    Returns:
        Voter -- Object for running votes
    """
    
    def __init__(self, voting_type):
        """initialize voter
        
        Arguments:
            voting_type {string} -- the voting mechanism to use (see docs)
        """
        super().__init__()
        self.valid_voting_types = [
        'accuracy', 'Penrose', 'maj_rule'
        ]
        assert voting_type in self.valid_voting_types
        self.voting_type = voting_type
        
    def predict(self, model_collection, date, test_mode=False, verbose=False):
        """make a prediction of the data for a given model_collection
        
        Arguments:
            model_collection {ModelCollection} -- Object to predict with
            date {datetime} -- set of data to make predict of
        
        Returns:
            (int, float) -- predicted class and models accuracy in tuple
        """
        if verbose:
            print(date)
        #get predictions, metrics
        model_predictions = model_collection.predict(date, verbose)
        if(test_mode):
            model_collection.get_voter_metrics()
            # model_metrics = [model.metrics for model in model_collection.models]
            # print(model_metrics)
        
        if verbose:
            print("Model Predictions: ", model_predictions)
        
        predictions = {}
        for i,model in enumerate(model_collection.models):
            if(test_mode):
                predictions[model.title] = (model_predictions[i], model.metrics['acc'], model.metrics['balance'], model.metrics['False Positive Rate'],model.metrics['pop'])
            else:
                predictions[model.title] = (model_predictions[i], model.metrics['acc'])

        
        if verbose:
            print("Updated Predictions in Voter", predictions)
        
        if self.voting_type == "maj_rule":
            
            total_votes = 0
            votes_toPass= 0
            votes_toReject =0

            for title, metrics in predictions.items():
                pred = metrics[0]
                votes = 1

                if pred == 0.0:
                    vote_to = 'reject'
                    votes_toReject += votes

                elif pred == 1.0:
                    vote_to = 'Pass'
                    votes_toPass += votes
               
                else:
                    print("your vote is not valid")

                total_votes += votes

                print(title + ' casts %d votes to %s ' %(votes,vote_to))
            
            ratio = votes_toPass/total_votes

            if ratio > .5:
                prediction = 1
            else:
                prediction = 0
        
        
        elif self.voting_type == "accuracy":
            total_votes =0
            votes_toPass= 0
            votes_toReject =0

            for title, metrics in predictions.items():
                pred = metrics[0]
                acc = metrics[1] 

                votes = int(acc*100)

                if pred ==0.0 :
                    vote_to = 'reject'
                    votes_toReject += votes
                elif pred== 1.0:
                    vote_to = 'Pass'
                    votes_toPass += votes
                else:
                    print("your vote is not valid")
                total_votes += votes
                
                print(title + ' casts %d votes to %s ' %(votes,vote_to))
            
            ratio = votes_toPass/total_votes

            if ratio > .5:
                prediction = 1
            else:
                prediction = 0

        elif self.voting_type == 'Penrose':
            total_votes =0
            votes_toPass= 0
            votes_toReject =0

            for title, metrics in predictions.items():
                pred = metrics[0]
                acc = metrics[1] 
                balance = metrics[2] 
                FPR = metrics[3] 
                pop = metrics[4]

                multiplier = math.exp((acc)) * (math.sqrt((1/balance)*(1/FPR)*(pop)))
                votes = int(multiplier)

                if pred ==0.0 :
                    vote_to = 'reject'
                    votes_toReject += votes
                elif pred == 1.0:
                    vote_to = 'Pass'
                    votes_toPass += votes
                else:
                    print("your vote is not valid")
                total_votes += votes

                print(title + ' casts %d votes to %s ' %(votes,vote_to))
            
            ratio = votes_toPass/total_votes
            if ratio > .5:
                prediction = 1
            else:
                prediction = 0
        
        
        else:
            prediction = 'you have not selected a valid voting method'
        
        if verbose:
            print("Voting Output ", prediction, " for model with accuracy ", model_collection.accuracy)
        
        return (prediction, model_collection.accuracy)
