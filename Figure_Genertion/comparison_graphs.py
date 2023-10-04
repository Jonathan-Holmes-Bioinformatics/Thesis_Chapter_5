import os
import sys
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt


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
	if "Bottleneck_Statistics" not in F:
		Rep_ID.append("Repeat: " + F[F.index("_") + 1:])
		for i in os.listdir(sys.argv[1] + "/" + F):
			if ".txt" in i:
				file = open(sys.argv[1] + "/" + F + "/" + i).read().split("Round")
				Phasotypes.append(file[1].split("\n")[2].split("\t")[1:])
				Initial_Matrix.append(to_float(file[1].split("\n")[1].split("\t")[1:]))
				Final_Dist_Matrix.append(to_float(file[-1].split("\n")[3].split("\t")[1:]))

i = 0

Transformed_Final_Dist = []

while i < len(Final_Dist_Matrix[0]):
	b = []
	for I in Final_Dist_Matrix:
		b.append(I[i])
	Transformed_Final_Dist.append(b)
	i = i + 1


for i in Transformed_Final_Dist:
	Means.append(np.average(i))
	SDs.append(np.std(i))


width = 0.35
fig, ax = plt.subplots()
ax.bar(Phasotypes[0], Initial_Matrix[0], width, label="Initial Distribution")
ax.bar(Phasotypes[0], Means, width, yerr=SDs, bottom=Initial_Matrix[0], label="Final Distribution")
ax.legend()
ax.set_title(sys.argv[1])
plt.xticks(rotation=90)
plt.savefig(sys.argv[1] + "/" + "Distributions")
plt.close()


























