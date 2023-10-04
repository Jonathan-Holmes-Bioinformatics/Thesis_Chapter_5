import os
import sys

Selection = sys.argv[2].split(",")


for doc in os.listdir(sys.argv[1]):
	if ".txt" not in doc and "Bottleneck" not in doc:
		for file in os.listdir(sys.argv[1] + "/" + doc):
			if "report" in file:
				input_file = open(sys.argv[1] + "/" + doc + "/" + file).read().split("Round")[1:]
				pheno_dist_step = []


				for R in input_file:
					FD = R.split("\n")[3].split("\t")[1:]
					pheno_dist_step.append(FD)


				sorted_dist = []

				for i in (input_file[0].split("\n")[1].split("\t")[1:]):
					sorted_dist.append([float(i)])


				for I in range(0,len(pheno_dist_step[0])):
					C = []
					for i in range(0,len(pheno_dist_step)):
						C.append(float(pheno_dist_step[i][I]))
					sorted_dist[I] = sorted_dist[I]  + C

				phasotypes = input_file[0].split("\n")[2].split("\t")[1:]
			
				BN =  [] 
					
				for i in input_file:
					BN.append(i.split("\n")[6].split("\t")[1:][0])

				import numpy as np
				import pandas as pd
				import matplotlib.pyplot as plt



				if len(phasotypes) > 8:
					fig, ax = plt.subplots(1, figsize = (16,9))
				else:
					fig, ax = plt.subplots(1)					

				pos = 0

				Selection = Selection*int(len(sorted_dist[0])/len(Selection))

				for i in sorted_dist:
					ax.plot(i, label = phasotypes[pos], linestyle = "dashdot")
					pos = pos + 1
				p = 0
				for s in Selection:
					if s == "NS":
						ax.hist([p,p+1],1,color = "lightgray")
					p = p + 1
				
				B = 0
				for b in BN:
					if b == "YES":
						ax.plot([B+1, B + 1],[0, 1], linestyle = "dashed", color = "red",alpha=0.5)
					B = B + 1
				ax.set_xlim([0, len(Selection)])
				ax.set_ylim([0, 1])
				ax.set_xlabel('No. Generations')
				ax.set_ylabel('Distribution of Phasotype')
				ax.legend(loc='upper right')
				ax.spines['left'].set_bounds(0, 1)
				ax.spines['right'].set_visible(False)
				ax.spines['top'].set_visible(False)
				if len(sorted_dist[0]) < 22:
					ax.set_xticks(range(0,len(sorted_dist[0])))
				elif len(sorted_dist[0]) < 100:
					ax.set_xticks(range(0,len(sorted_dist[0]),10))
				else:
					ax.set_xticks(range(0,len(sorted_dist[0]),20))
				plt.grid(axis = 'x',linestyle = '--', linewidth = 0.25, color = "black")
				plt.savefig(sys.argv[1] + "/" + doc + "/" + "/Combined")
				plt.close()


























