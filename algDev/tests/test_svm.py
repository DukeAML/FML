from algDev.algorithms.svm import SVM
import numpy as np
import pickle
def run():
    X = np.zeros((5,2))
    y = np.zeros((5,))

    y[3] = 1
    y[4] = 1

    X[0,:] = [-2,4]
    X[1,:] = [-1,1]
    X[2,:] = [0,0]
    X[3,:] = [1,1]
    X[4,:] = [2,4]

    svm = SVM(X=X, y=y, params= {'C': 1, 'gamma' :0.1})

    svm.train([1,0], verbose=True)

    print(svm.predict([[3,9]]))

def run_2():
    X = np.zeros((5,2))
    y = np.zeros((5,))

    y[3] = 1
    y[4] = 1

    X[0,:] = [-2,4]
    X[1,:] = [-1,1]
    X[2,:] = [0,0]
    X[3,:] = [1,1]
    X[4,:] = [2,4]

    svm = SVM(X=X, y=y, params= {'C': 1, 'gamma' :0.1})

    svm.train([1,0], verbose=True)

    modelData = pickle.dumps(svm.model)

    saved_data = pickle.loads(modelData)

    new_svm = SVM(model=saved_data)

    print(new_svm.predict([[3,3]]))


    


    