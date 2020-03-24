from sklearn import svm
from build_dfFeatures import gen_features
from gen_indicators import gen_data
from svm import svm_collection

def predict(eq, features, days, look_back, binary_category, threshold, verbose= False, voting_type, new_data):
    
    models = svm_collection(eq, features, days, look_back, binary_category, threshold, verbose)

    for model in models:
        #predict on new data
        #put somewhere

    #based on voting type ...

    #combine prediction with acc from models - return final prediction
    acc = 0  #filler
    prediction = acc #filler

    return prediction