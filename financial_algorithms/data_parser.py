import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

df = pd.read_csv("VSLR.csv")

closes = []
highs = []
lows = []

for index, row in df.iterrows():
    closes.append(float(row["Close"]))
    lows.append(float(row["Low"]))
    highs.append(float(row["High"]))

plt.plot(closes, 'b-')
plt.plot(lows, 'r-')
plt.plot(highs, 'g-')

# plt.show()

features = []
labels = []

for index, close in enumerate(closes):
    if(index > (len(closes) - 11)):
        break
    feature = []
    for i in range(9):
        feature.append(np.sign(closes[index + i + 1] - closes[index + i]))
    if(closes[index + 10]-closes[index+9] > 0):
        label = 1
    else:
        label = 0
    features.append(feature)
    labels.append(label)

features = np.array(features)
print(features)
labels = np.array(labels)
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=0)
model = SVC(kernel='linear', probability=True)
model.fit(X_train, y_train)
prediction = model.score(X_test, y_test)
print(prediction)
