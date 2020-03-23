from sklearn import svm
from build_dfFeatures import gen_features
from gen_indicators import gen_data
#this is the file for running all versions of svm-model based voting algorithms

#20-50 svm models 
#features: combo (small bucket) of indicator, maybe only one 
#binary category is either: postive, negative, or window


def function(eq, features, days, look_back, binary_category, threshold):
    '''
    inputs:
        eq: (string) ticker for equity of interest 
        features: (list of list of strings), each list is all predictive features wanted for a model
        days: number of days to use
        look_back: period of interest for meeting return criterion (did eq return ever surpass 2% inc within look_back days)
        binary category: one of "postive", "negative", or "window". positive establishes upper threshold, 
                        negative establishes lower threshold, and window establishes upper and lower threshold 
        threshold: limit of interest. (does return on equity surpass, fall beneath, etc. threshold)
    outputs:
        models: a dictionary of models, one for each set of features, and their accuracies
                keys = indices based on feature sets
                values = tuples of the form (model, accuracy)


    '''
    model_data = []

    for feature_list in features:
        X_train, y_train, X_test, y_test = gen_data(eq, feature_list, days, look_back, binary_category, threshold)
        model_data.append([X_train, y_train, X_test, y_test])
    
    models ={}
    index =0
    for data_set in model_data:
        X_train = data_set[0]
        y_train = data_set[1]
        X_test = data_set[2]
        y_test = data_set[3]
        clf = svm.SVC(gamma = "auto")
        clf.fit(X_train, y_train)
        acc = clf.score(X_test, y_test)
        models[index] = (clf, acc)

        index+=1 
    
    return models


    




