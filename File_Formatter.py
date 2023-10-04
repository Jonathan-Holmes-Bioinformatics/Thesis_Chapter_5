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
#		This script is designed to be imported into other scripts using import File_Formatter
#			
#
# ------------------------------------------------------------------------------------------------

# Required libraries
import os
import sys


# In built functions
def str_to_float(A):
	B = []	
	for i in A:
		B.append(float(i))
	return(B)


# Input is an input file (for model) the function will read the file and output a list of the variables
def Reader(file):
	Read = open(file).read().split("#")
	Repeats = Read[1].replace("Repeat","").replace("\n","").replace(",","")
	Max_Gen = Read[2].replace("Max Gen","").replace("\n","").split(",")
	Generations  = Read[3].replace("Generations","").replace("\n","").split(",")
	Initial_Dist = Read[4][Read[4].index("\n"):].replace("\n","").split(",")
	Mutation_Rate =[x for x in  Read[5].split("\n")[2:] if x]
	Selection_Rate = [x for x in Read[6].split("\n")[2:] if x]
	Bottleneck = [x for x in (Read[7].replace("Bottleneck","").replace("\n","").split(",")) if x]
	Replicates = Read[8].replace("Replicates","").replace(",","").replace("\n","")
	return Repeats,Max_Gen,Generations,Initial_Dist,Mutation_Rate,Selection_Rate,Bottleneck,Replicates



# This function will create an input file based on variables supplied 
def Writer(file,Repeats,Max_Gen,Generations,Initial_Dist,Mutation_Rate,Selection_Rate,Bottleneck,Replicates):
	new_file = open(file,"w")
	Repeat_in = "#Repeat\n" + str(Repeats)
	Max_Gen_in = "#Max Gen\n"  +",".join(Max_Gen) 
	Generations_in = "#Generations\n" + ",".join(Generations)
	Initial_Dist_in = "#Initial_Distribution\n" + ",".join(Initial_Dist)
	Mutation_Rate_in = "#Mutation Rate\n"  + "OFF - ON,ON - OFF,"*int((len(Mutation_Rate[0].split(","))/2)) + "\n" + "\n".join(Mutation_Rate)
	Selection_Rate_in = "#Selection Rate\n" + "OFF  ,ON"*int((len(Selection_Rate[0].split(","))/2)) + "\n" + "\n".join(Selection_Rate)
	Bottleneck_in = "#Bottleneck\n" + ",".join(Bottleneck)
	Replicates_in = "#Replicates\n" + str(Replicates) + "\n"
	new_file.write(Repeat_in + "\n" + Max_Gen_in + "\n" + Generations_in + "\n" + Initial_Dist_in + "\n" + Mutation_Rate_in + "\n" + Selection_Rate_in + "\n" + Bottleneck_in + "\n" + Replicates_in)
	new_file.close()

# This will extract the final output data from a modelled runs folder
def Extract_Results(folder):
	runs = os.listdir(folder)
	results = []
	for run in runs:
		if "Rep" in run:
			output_data = open(folder + "/" + run + "/" + folder + "_report.txt").read().split("Round")[-1].split("\n")[3].split("\t")[1:]
			results.append(str_to_float(output_data))
	return(results)















