import os
import sys
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt

Input_folder = os.listdir(sys.argv[1])


def to_int(a):
	b = []
	for i in a:
		b.append(int(i))
	return(b)
for doc in Input_folder:
	if ".txt" not in doc and "Bottleneck" not in doc:
		for file in os.listdir(sys.argv[1] + "/" + doc):

			if "report" in file:


				File = open(sys.argv[1] + "/" + doc + "/" + file).read().split("Round")[1:]
				Data = []
				Stationary = []
				title = File[0].split("\n")[2].split("\t")[1:]
				S = (File[0].split("\n")[1].split("\t")[1:])
				for i in S:
					Data.append([float(i)])

				for line in File:
					Final = line.split("\n")[3].split("\t")[1:]	
					pos = 0
					for i in Final:
						Data[pos].append(float(i))
						pos = pos + 1
					Stationary.append(int(line.split("\n")[5].split("\t")[1:][0]))

	
				cols = 0
				rows = 0


				if len(title) > 8:	
					for i in range(1,int(len(title)/2)):
						if len(title) % i == 0:
							rows = i
					cols = int(len(title)/rows)
					fig, axs  = plt.subplots(rows, cols, figsize = (16, 9), constrained_layout=True)

				else:
					for i in range(1,len(title)):
						if len(title) % i == 0:
							rows = i
					cols = int(len(title)/rows)
					fig, axs  = plt.subplots(rows, cols, constrained_layout=True)

				i = 0
				s = 0

				for i in range(0,rows):
					for I in range(0,cols):
						axs[i,I].plot(Data[s])
						axs[i,I].set_ylim([0,1])
						axs[i,I].set_title(title[s])
						s = s + 1
				plt.savefig(sys.argv[1] + "/" + doc + "/" + "/Distributions")
				plt.close()

				fig2, ax2  = plt.subplots(1, figsize = (16, 9))

				ax2.bar(range(len(Stationary)), Stationary, color='royalblue', alpha=0.7)
				ax2.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
				plt.savefig(sys.argv[1] + "/" + doc + "/" + "/Stationary")
				plt.close()







