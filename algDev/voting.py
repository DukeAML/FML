from sklearn import svm
from build_dfFeatures import gen_features
from gen_indicators import gen_data
from svm import svm_collection

def predict(eq, features, days, look_back, binary_category, threshold, voting_type, new_data, verbose= False,):
    '''
    this function returns a final prediction 

    inputs:
        eq: (string) ticker for equity of interest 
        features: (list of list of strings), each list is all predictive features wanted for a model
        days: number of days to use
        look_back: period of interest for meeting return criterion (did eq return ever surpass 2% inc within look_back days)
        binary category: one of "postive", "negative", or "window". positive establishes upper threshold, 
                        negative establishes lower threshold, and window establishes upper and lower threshold 
        threshold: limit of interest. (does return on equity surpass, fall beneath, etc. threshold)
        verbose: bool, print dimensions of data if True
        voting_type: one of below 
            "accuracy_based": 

        new_data: 1 day of data to predict on ! 
    outputs:
        prediction: binary variable, final prediction for eq given labels, models, voting method, etc. 

    '''

    
    models = svm_collection(eq, features, days, look_back, binary_category, threshold, verbose)

    predictions ={}
    sum_predict = 0
    index = 1 #start at one so that last index is #total models
    for model in models.items():
        clf = model[0]
        prediction = clf.predict(new_data)
        sum_predict += prediction
        predictions[index] = (prediction, model[1])
        index += 1
    
    if voting_type == "accuracy_based":

        sum_voting = 0
        sum_acc =0
        for entry in predictions.items():
            sum_voting += entry[0]*entry[1]
            sum_acc += entry[1]
        
        normalized = sum_voting/sum_acc

        if normalized > .5:
            prediction = [1]
        
        else:
            prediction = [0]
    
    else:
        prediction = 'you have not selected a valid voting method'


    return prediction