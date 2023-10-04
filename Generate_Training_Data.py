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
# 		Generates training data for machine learning alogrithms
#
# 		python3 generated_training_data.py Output_file.csv
#
# ------------------------------------------------------------------------------------------------

# Reequired librares - popstats avalible from: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5380846/   File_Formatter avalible from: https://github.com/Jonathan-Holmes-Bioinformatics/Thesis_Chapter_5
import os
import popstats   
import File_Formatter
import random
import skbio
from scipy.spatial import distance
import itertools
import sys


# In built functions
def to_float(A):
	B = []
	for i in A:
		B.append(float(i))
	return B

def to_string(A):
	B = []
	for i in A:
		B.append(str(i))
	return B

def ON_Ratio(dist,phasomes):
	ON_Dist = []

	for gene in range(0,len(phasomes[0])):
		pos = 0			
		ON = 0
		OFF = 0
		for p in phasomes:
			if p[gene] == "1":
				ON = ON + dist[pos]
			pos = pos + 1
		ON_Dist.append(ON)

	return ON_Dist

def phasome(A):
	E = []
	for B in A:
		C = ""
		for D in B:
			C = C + str(D)
		E.append(C)
	return E

def normalise(A):
	B = []

	for i in A:
		B.append(round(float(i)/sum(A),3))
	return B

# open output file
Output = open(sys.argv[1] + ".txt","w")


# Run for N generations
# Requires input file from :  https://github.com/Jonathan-Holmes-Bioinformatics/Thesis_Chapter_5
for iter in range(1,200000):
	print(iter)


	Repeats,Max_Gen,Generations,Initial_Dist,Mutation_Rate,Selection_Rate,Bottleneck,Replicates = File_Formatter.Reader("Neutral_Input.csv")

	# define range of generations
	New_Generations = float(random.randrange(1,20))

	# Define new bottleneck size (random choice)
	new_bottleneck = [Bottleneck[0], str(random.choice([1,2,4,8,16,32,64,128])), Bottleneck[-1]]	

	# Define random selection coefficient
	new_selection_rate = []
	sel_output = []
	for i in Selection_Rate:	

		S = random.randrange(90,110)/100
		if S < 1:
			new_S = 2 - S
			new_selection_rate.append(str(new_S) + ",1")		
		if 1 <= S:
			new_selection_rate.append("1," + str(S))
		sel_output.append(str(float(S)))

	input_dist = [0]*len(Initial_Dist)

	# Create random population
	for i in range(0,len(input_dist)):
		p = random.randint(30, 70)
		input_dist[i] = input_dist[i] + p

	new_input_dist = to_string(normalise(input_dist))

	# Generated new temp_file
	File_Formatter.Writer(sys.argv[1] + ".csv",Repeats,Max_Gen,New_Generations,new_input_dist,Mutation_Rate,new_selection_rate,new_bottleneck,Replicates)
	
	
	# Run model # Requires Run_Model.py and other files from:  https://github.com/Jonathan-Holmes-Bioinformatics/Thesis_Chapter_5
	os.system("python3 Run_Model.py " + sys.argv[1] + ".csv " + sys.argv[1])

	output = File_Formatter.Extract_Results(sys.argv[1])

	os.system("rm " + sys.argv[1] + ".csv")
	os.system("rm -r "  + sys.argv[1])

	# Writing output vairiables and input variables to training data file
	Diversity = skbio.diversity.alpha.simpson(output[0])
	Divergence = popstats.calculateDivergence(to_float(new_input_dist), output[0])
	Start_Diversity = skbio.diversity.alpha.simpson(to_float(new_input_dist))

	Phasomes = []
	for y in range(0,10):
		if len(phasome(list(itertools.product([0, 1], repeat=y)))) == len(Initial_Dist):
			Phasomes = phasome(list(itertools.product([0, 1], repeat=y)))

	output_on_per = (ON_Ratio(output[0],Phasomes))
	input_on_per = (ON_Ratio(to_float(new_input_dist),Phasomes))


	output_line =  [int(new_bottleneck[1])] + [float(Diversity)] + [float(Divergence)] + [float(Start_Diversity)] + output_on_per + input_on_per + sel_output
	Output.write("\t".join(to_string(output_line)) + "\n")


Output.close()





