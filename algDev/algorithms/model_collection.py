from algorithms.svm import SVM
from algorithms.cnn import CNN
from models.equity import Equity
from preprocessing.data_generator import 
class MODEL_COLLECTION:
    
    def __init__(self, ticker, type, features, label_type):
        self.eq = Equity(ticker)
        self.features = create_features(self.eq, features, normalize = True, save = False)
        
        self.models = self.init_models(type)

    # def init_models(self, type):
    #     if type=='cnn':
            

    #     elif type=='svm':