import os
import sys
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import skbio
import scipy







Folders = os.listdir(sys.argv[1])

def to_float(a):
	b = []
	for i in a:
		b.append(float(i))
	return b
	

Initial_Matrix = []

Phasotypes = []


Final_Dist_Matrix = []

Means = []

SDs = []

Rep_ID = []
for F in Folders:
	if "Bottleneck_Statistics" not in F and "Distributions" not in F and ".png" not in F:		
		Rep_ID.append("Repeat: " + F[F.index("_") + 1:])
		for i in os.listdir(sys.argv[1] + "/" + F):
			if ".txt" in i:
				file = open(sys.argv[1] + "/" + F + "/" + i).read().split("Round")
				Phasotypes.append(file[1].split("\n")[2].split("\t")[1:])
				Initial_Matrix.append(to_float(file[1].split("\n")[1].split("\t")[1:]))
				Final_Dist_Matrix.append(to_float(file[-1].split("\n")[3].split("\t")[1:]))




Diversity = []
entropy  = []
Diversity_s = []
entropy_s  = []
"""
Scipy's entropy function will calculate KL divergence if feed two vectors p and q, each representing a probability distribution. If the two vectors aren't pdfs, it will normalize then first.
"""

for i in Final_Dist_Matrix:
	Diversity_s.append(skbio.diversity.alpha.shannon(i))
	entropy_s.append(scipy.stats.entropy(i,Initial_Matrix[0]))


for i in Diversity_s:
	Diversity.append(i/max(Diversity_s))
for i in entropy_s:
	entropy.append(i/max(entropy_s))


combined_1 = []
i = 0
for I in Diversity:
	combined_1.append([I,entropy[i]])
	i = i + 1

combined = np.array(combined_1)

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler

	
cols = ["black","grey","red","peru","orange","gold","yellowgreen","lime","cyan","dodgerblue","navy","blueviolet","violet","fuchsia","deeppink","crimson"]*10



db = DBSCAN(eps=0.3, min_samples=10).fit(combined)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

import matplotlib.pyplot as plt

unique_labels = set(labels)


colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]


for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = combined[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)

    xy = combined[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)
plt.title(sys.argv[1] + "\n" +'Estimated number of clusters: %d' % n_clusters_)
plt.savefig(sys.argv[1] + "/Cluster_Graph")

















