from gen_lstm_data import gen_data
from sklearn import manifold
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
(X_train, y_train, X_test, y_test) = gen_data(eq = "AAPL", verbose= True)

X_train = X_train.reshape((len(X_train), 19*25))

a = y_train[:,0]==1
b = y_train[:,1]==1
c = y_train[:,2]==1
d = y_train[:,3]==1
e = y_train[:,4]==1
f = y_train[:,5]==1
g = y_train[:,6]==1
h = y_train[:,7]==1
i = y_train[:,8]==1
j = y_train[:,9]==1

tsne = manifold.TSNE(perplexity=50, n_iter=2000)
Y = tsne.fit_transform(X_train)

plt.scatter(Y[a,0], Y[a,1], c="r")
plt.scatter(Y[b,0], Y[b,1], c="r")
plt.scatter(Y[c,0], Y[c,1], c="r")
plt.scatter(Y[d,0], Y[d,1], c="r")
plt.scatter(Y[e,0], Y[e,1], c="k")
plt.scatter(Y[f,0], Y[f,1], c="b")
plt.scatter(Y[g,0], Y[g,1], c="b")
plt.scatter(Y[h,0], Y[h,1], c="b")
plt.scatter(Y[i,0], Y[i,1], c="b")
plt.scatter(Y[j,0], Y[j,1], c="b")

fig = plt.gcf()
fig.savefig('test.png', dpi=100)
