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
	

IDs = [] 
phasotypes = []
initial_inputs = []
final_output = []


for F in Folders:
	run_data = []
	initial_data = []
	PT = []
	if ".png" not in F:
		for sub_f in (os.listdir(sys.argv[1] + "/" + F)):
			if "Bottleneck_Statistics" not in sub_f and "Distributions" not in sub_f and ".png" not in sub_f:
				IDs.append(F)
				for i in os.listdir(sys.argv[1] + "/" + F + "/" + sub_f):
					if ".txt" in i:
						file = open(sys.argv[1] + "/" + F + "/" + sub_f + "/" + i).read().split("Round")
						PT.append(file[1].split("\n")[2].split("\t")[1:])
						initial_data.append((to_float(file[1].split("\n")[1].split("\t")[1:])))
						run_data.append(to_float(file[-1].split("\n")[3].split("\t")[1:]))
		initial_inputs.append(initial_data)
		final_output.append(run_data)
		phasotypes.append(PT)



Diversity_s = []
entropy_s  = []


pos = 0
for i in final_output:
	pos2 = 0
	for I in i:
		Diversity_s.append(skbio.diversity.alpha.shannon(I))
		entropy_s.append(scipy.stats.entropy(I,initial_inputs[pos][pos2]))
		pos2 = pos2 + 1
	pos = pos + 1

"""
Scipy's entropy function will calculate KL divergence if feed two vectors p and q, each representing a probability distribution. If the two vectors aren't pdfs, it will normalize then first.
"""

Diversity = []
entropy = []
for i in Diversity_s:
	Diversity.append(i/max(Diversity_s))
for i in entropy_s:
	entropy.append(i/max(entropy_s))


from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler

combined_l = []

i = 0
for I in Diversity:
	combined_l.append([I,entropy[i]])
	i = i + 1


combined = np.array(combined_l)



db = DBSCAN(eps=0.3, min_samples=10).fit(combined)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

"""
print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(Rep_ID, labels))
print("Completeness: %0.3f" % metrics.completeness_score(Rep_ID, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(Rep_ID, labels))
print("Adjusted Rand Index: %0.3f" % metrics.adjusted_rand_score(Rep_ID, labels))
print("Adjusted Mutual Information: %0.3f"% metrics.adjusted_mutual_info_score(Rep_ID, labels))
print("Silhouette Coefficient: %0.3f"% metrics.silhouette_score(combined, labels))
"""

import matplotlib.pyplot as plt

# Black removed and is used for noise instead.
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

plt.title(sys.argv[1] + "\n" +  'Estimated number of clusters: %d' % n_clusters_)
plt.savefig(sys.argv[1]  + "/" + "Clustered_plot")
plt.close()


unique_IDs = []

for i in IDs:
	if i not in unique_IDs:
		unique_IDs.append(i)

unique_IDs.sort()

labels = []
cols = ["black","grey","red","peru","orange","gold","yellowgreen","lime","cyan","dodgerblue","navy","blueviolet","violet","fuchsia","deeppink","crimson"]*10


for i in IDs:
	labels.append(cols[unique_IDs.index(i)])

scatter_matrix = []

for ID in unique_IDs:
	l = [[],[]]
	L = 0
	for I in IDs:
		if I == ID:
			l[0].append(combined_l[L][0])
			l[1].append(combined_l[L][1])
		L = L + 1
	scatter_matrix.append(l)



colors = []
for i in range(0,len(unique_IDs)):
	colors.append(cols[i])

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)


for data, color, group in zip(scatter_matrix, colors, unique_IDs):
	x, y = data
	ax.scatter(x, y, alpha=0.5, c=color, edgecolors='none', s=60, label=group)
plt.title(sys.argv[1])
plt.legend(loc="best")
plt.savefig(sys.argv[1] + "/" + "dotplot")






#https://scikit-learn.org/stable/auto_examples/cluster/plot_affinity_propagation.html#sphx-glr-auto-examples-cluster-plot-affinity-propagation-py



