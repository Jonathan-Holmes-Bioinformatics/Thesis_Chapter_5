# -----------------------------------------------------------------------------------------------
# 
#
#
# Jonathan Holmes
#
# Permission to use, copy, modify, and/or distribute this software or any part thereof for any
# purpose with or without fee is hereby granted provided that:
#     (1) the original author is credited appropriately in the source code
#         and any accompanying documentation
# and (2) that this requirement is included in any redistribution.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
# SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
# OF THIS SOFTWARE.
#
# E-mail: jh795@leicester.ac.uk
# ------------------------------------------------------------------------------------------------
# 
#
#		To Run this script use:
#		python3 Run_Model.py Input_file.csv Output_folder
# 
#
# ------------------------------------------------------------------------------------------------


# Required Libraries
import os
import sys
import numpy
import time	
import itertools
import random
import Mutation_Selection_Model as MM
localtime = time.localtime(time.time())
stattol=0.00001



# In built functions

def to_str(a):
	b = []
	for i in a:
		b.append(str(i))
	return b


def to_int(a):
	b = []
	for i in a:
		b.append(float(i))
	return b

def bottleneck(a,b,c,d,e,f):
	phase = [i for i in range(len(b))]
	new_pop = [0]*len(phase)
	for i in range(0,int(a[1])):
		#new_pop.append()
		sel = numpy.random.choice(phase,1, p=b)
		new_pop[sel[0]] = new_pop[sel[0]] + 1
	
	new_dist = []
	
	for i in new_pop:
		new_dist.append(i/sum(new_pop))

	output_file = open(sys.argv[2] + "/Bottleneck_Statistics/report.txt","a")	
	
	output_file.write("\nReplicate:\t" + str(d) + "\nCycle:\t" + str(f) + "\nInital Distribution:\t" + "\t".join(to_str(b)) + "\nOutput_Distribution:\t" + "\t".join(to_str(new_dist)) + "\n")

	output_file.close()

	return(new_dist)


def empty_var(a):
	b = []
	for i in a:
		if len(i) != 0:
			b.append(float(i))

	return(b)

def transformation(a):
	set_len = int(len(empty_var(a[0].split(",")))/2)
	c = []
	l = 0
	for i in range(0,set_len):
		b = []
		for I in a:
			row = (empty_var(I.split(","))[:])
			b.append(row[l:l+2])
		l = l + 2
		c.append(b)
	return(c)


# Define input file and create data holdings
input_file = open(sys.argv[1]).read().split("#")[1:]
Bottleneck = []
NS_S = []

# Read input file
for variable in input_file:
	var = variable.split("\n")[:-1]
	if "Repeat" in var[0]:
		Repeat = str(var[1].split(",")[0])
	if "Max Gen" in var[0]:
		Max_Gen = empty_var(var[1].split(","))
	if "Generations" in var[0]:
		Generations = empty_var(var[1].split(","))
	if "Mutation Rate" in var[0]:
		Mutation_Rate = transformation(var[2:])
	if "Selection Rate" in var[0]:
		Selection = transformation(var[2:])
	if "Initial_Distribution" in var[0]:
		Distribution = [to_int(empty_var(var[1].split(",")))]
	if "Bottleneck" in var[0]:
		for i in var[1].split(","):
			if len(i) != 0:
				Bottleneck.append(i)
	if "Replicates" in var[0]:
		Replicate = empty_var(var[1].split(","))[0]

# Define selective cycles
for sel in Selection:
	all_sel = (list(itertools.chain.from_iterable(sel)))
	if sum(all_sel) == len(all_sel):
		NS_S.append("NS")
	else:
		NS_S.append("S")

# Input data Sanity checks
# Check that phasotypes sum to close to 1.
if sum(Distribution[0]) <= 0.99:
	if sum(Distribution[0]) >= 1.01:
		print("Initial Distribution not equal to 1\t(" + str(sum(Distribution[0])) + ")")
		exit()

# Checks mutation and selection apply to all genes
if len(Selection[0]) != len(Mutation_Rate[0]):
	print("Error in input: Please fix")
	exit()
else:
	No_genes = len(Selection[0])


# Creates otuput folder
if "/" in sys.argv[2]:
	sub_name = sys.argv[2].split("/")[1]
	if sys.argv[2].split("/")[0] not in os.listdir():
		os.mkdir(sys.argv[2].split("/")[0])
else:
	sub_name = sys.argv[2]


# Checks name of output folder not taken
if sys.argv[2] in os.listdir():
	print("folder already in use: Please choose a different name.")
	exit()
else:
	os.mkdir(sys.argv[2])
	os.mkdir(sys.argv[2] + "/Bottleneck_Statistics")
	bottleneck_stats = open(sys.argv[2] + "/Bottleneck_Statistics/report.txt","w")
	bottleneck_stats.write(str(localtime) + "\n")
	bottleneck_stats.close()

# Starts model
print("Running Model")

# Runs through reach repitition of model
for rep in (range(0,int(Replicate))):
	os.mkdir(sys.argv[2] + "/Rep_" + str(rep))
	Ref_file = open(sys.argv[2] +  "/Rep_" + str(rep) +"/" + sub_name + "_report.txt","w")
	Ref_file.write("Report generated" + str(localtime) + "\n")
	Ref_file.close()
	cycle = 0
	Distribution_2 = [Distribution[0]]
	for repeat in range(0,int(Repeat)):
		BN = []
		for i in range(0,len(Max_Gen)):
			new_Dist = []
			pqmat = numpy.array(Mutation_Rate[i])
			tensorrv2_pretensorTbl2_two_pre= Selection[i]
			rv2_preTbl2_tw0 = MM.tensorit(tensorrv2_pretensorTbl2_two_pre)
			gamma_mat = rv2_preTbl2_tw0[0]


			output = MM.mutsel_model(Distribution_2[cycle],pqmat,gamma_mat,int(float(Generations[i])),stattol,int(float(Max_Gen[i])),No_genes)



			if Bottleneck[0] != "0":
				if Bottleneck[2] == "R":

					

					if (cycle + 1) % int(Bottleneck[0]) == 0 and int(Bottleneck[0]) != 0 and cycle != int(Repeat)*len(Max_Gen) - 1:
						BN.append(1)
						new_Dist = bottleneck(Bottleneck, output[3], output[-2], rep, repeat, cycle)
						Distribution_2.append(new_Dist)
						B = "YES"
					else:
						Distribution_2.append(output[3].tolist())
						BN.append(0)
						B = "NO"
				if Bottleneck[2] == "N":
					if (cycle + 1) == int(Bottleneck[0]):
						BN.append(1)
						new_Dist = bottleneck(Bottleneck, output[3], output[-2], rep, repeat, cycle)
						Distribution_2.append(new_Dist)
						B = "YES"
					else:
						Distribution_2.append(output[3].tolist())
						BN.append(0)
						B = "NO"

			else:
				Distribution_2.append(output[3].tolist())
				B = "NO"	


			if type(output[4]) is not str:
				report = ("Round " + str(cycle + 1)  + "\nStarting Distribution:\t" + "\t".join([str(i) for i in Distribution_2[cycle]])) + "\nPhasotypes:\t" + "\t".join(output[-2]) + "\n" + "Final Distribution:\t" +  "\t".join([str(i) for i in output[3].tolist()]) + "\n" + "Stationary Distribution:\t" + "\t".join([str(i) for i in output[4].tolist()]) + "\nGenerations to Stationary Distribution:\t" + str(output[5]) + "\nBottleneck applied:\t" + B + "\n"*2
			else:	
				report = ("Round " + str(cycle + 1)  + "\nStarting Distribution:\t" + "\t".join([str(i) for i in Distribution_2[cycle]])) + "\nPhasotypes:\t" + "\t".join(output[-2]) + "\n" + "Final Distribution:\t" +  "\t".join([str(i) for i in output[3].tolist()]) + "\n" + "Stationary Distribution:\t" + "\t" + output[4] + "\nGenerations to Stationary Distribution:\t" + str(output[5]) + "\nBottleneck applied:\t" + B + "\n"*2
			Ref_file_new = open(sys.argv[2] +  "/Rep_" + str(rep) +"/" + sub_name + "_report.txt","a")		
			Ref_file_new.write(report)
			Ref_file_new.close()
			full_data = output[-1].tolist()

			Full = [[1] + Distribution_2[i]]
			count = 1
			for Round in full_data:
				if sum(Round) != 0:
					Full.append([count] + Round)
				count = count + 1

			output_file = open(sys.argv[2] + "/Rep_" + str(rep) + "/"  + sub_name + "_round_" + str(cycle) + ".csv","w")
			for line in Full:
				output_file.write("\t".join([str(i) for i in line]) + "\n")

			output_file.close()

			cycle = cycle + 1


## Unhash these lines to generate figure outputs where required.

#os.system("python3 Figure_Genertion/Initial.py " + sys.argv[2])
#os.system("python3 Figure_Genertion/Combined.py " + sys.argv[2] + " " + ",".join(NS_S))
#os.system("python3 Figure_Genertion/comparison_graphs.py " + sys.argv[2])
#os.system("python3 Figure_Genertion/Diversity_Divergence_local.py " + sys.argv[2])























