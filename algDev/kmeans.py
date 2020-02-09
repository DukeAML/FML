
from time import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

from gen_lstm_data import gen_data, gen_labels, get_data_labelled
import pandas as pd

np.random.seed(42)

#get data, labeled for every day
(X_train, y_train, X_test, y_test) = gen_data(eq = "VSLR", look_back =1, verbose= True)

#reshape to (N, 25) and scale
data = X_train.reshape(-1,25)
data = scale(data)

#change labels from one-hot to integer valued (for dimensions)
labels =[]
for label in y_train:
    if np.sum(label) != 0:
        for i in range(len(label)):
            if label[i] == 1:
                index = i  
    else: 
        index = -1
    labels.append(index)
labels = np.asarray(labels)

#confirm correct shapes
print(data.shape)
print(labels.shape)


n_samples, n_features = data.shape
n_strata = len(np.unique(labels)) #num classes

sample_size = 300

print("n_strata: %d, \t n_samples %d, \t n_features %d"
      % (n_strata, n_samples, n_features))


print(82 * '_')
print('init\t\ttime\tinertia\thomo\tcompl\tv-meas\tARI\tAMI\tsilhouette')

def bench_k_means(estimator, name, data):
    t0 = time()
    estimator.fit(data)
    print('%-9s\t%.2fs\t%i\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f'
          % (name, (time() - t0), estimator.inertia_,
             metrics.homogeneity_score(labels, estimator.labels_),
             metrics.completeness_score(labels, estimator.labels_),
             metrics.v_measure_score(labels, estimator.labels_),
             metrics.adjusted_rand_score(labels, estimator.labels_),
             metrics.adjusted_mutual_info_score(labels,  estimator.labels_),
             metrics.silhouette_score(data, estimator.labels_,
                                      metric='euclidean',
                                      sample_size=sample_size)))

bench_k_means(KMeans(init='k-means++', n_clusters=n_strata, n_init=10),
              name="k-means++", data=data)

bench_k_means(KMeans(init='random', n_clusters=n_strata, n_init=10),
              name="random", data=data)

# in this case the seeding of the centers is deterministic, hence we run the
# kmeans algorithm only once with n_init=1
pca = PCA(n_components=n_strata).fit(data)
bench_k_means(KMeans(init=pca.components_, n_clusters=n_strata, n_init=1),
              name="PCA-based",
              data=data)
print(82 * '_')      

# #############################################################################
# Visualize the results on PCA-reduced data

reduced_data = PCA(n_components=2).fit_transform(data)
kmeans = KMeans(init='k-means++', n_clusters=n_strata, n_init=10)
kmeans.fit(reduced_data)


# Step size of the mesh. Decrease to increase the quality of the VQ.
h = .02     # point in the mesh [x_min, x_max]x[y_min, y_max].

# Plot the decision boundary. For that, we will assign a color to each
x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# Obtain labels for each point in mesh. Use last trained model.
Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

# Put the result into a color plot
Z = Z.reshape(xx.shape)
plt.figure(1)
plt.clf()
plt.imshow(Z, interpolation='nearest',
           extent=(xx.min(), xx.max(), yy.min(), yy.max()),
           cmap=plt.cm.Paired,
           aspect='auto', origin='lower')

colors = []
for ii in range(len(reduced_data)):
    label = labels[ii]
    if label == -1:
        colors.append('y')
    elif label == 0:
        colors.append('y')
    elif label == 1:
        colors.append('y')
    elif label == 2:
        colors.append('y')
    elif label == 3:
        colors.append('w')
    elif label == 4:
        colors.append('w')
    elif label == 5:
       colors.append('w')
    elif label == 6:
        colors.append('k')
    elif label == 7:
        colors.append('k')
    elif label == 8:
        colors.append('k')
    elif label == 9:
        colors.append('k')
    elif label == 10:
        colors.append('k')

x= reduced_data[:, 0]
y = reduced_data[:, 1]
df = pd.DataFrame(dict(x=x , y = y, colors=colors))

plt.plot(df['x'], df['y'], 'k.', c = df['colors'], markersize=2)

# plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)

# Plot the centroids as a white X
centroids = kmeans.cluster_centers_
plt.scatter(centroids[:, 0], centroids[:, 1],
            marker='x', s=169, linewidths=3,
            color='w', zorder=10)
plt.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
          'Centroids are marked with white cross')
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())
plt.show()
