import os
import sys


Folder = sys.argv[1].split("/")[0]

Cluster = []
Distributions = []


for folder in os.listdir(Folder):
	if ".png" not in folder:
		for file in os.listdir(Folder + "/" + folder):
			if file == "Distributions.png":
				Distributions.append(Folder + "/" + folder + "/" + file)
			if file == "Cluster_Graph.png":
				Cluster.append(Folder + "/" + folder + "/" + file)


from PIL import Image



Cl = [Image.open(x) for x in Cluster]
Dis = [Image.open(x) for x in Distributions]

widths, heights = zip(*(i.size for i in Dis))

total_width = sum(widths)
max_height = max(heights)


comb_Cl = Image.new('RGB', (total_width, max_height))
comb_Dis = Image.new('RGB', (total_width, max_height))

x_offset = 0
for im in Cl:
  comb_Cl.paste(im, (x_offset,0))
  x_offset += im.size[0]

comb_Cl.save(Folder + '/Combined_Cluster.png')

x_offset = 0
for im in Dis:
  comb_Dis.paste(im, (x_offset,0))
  x_offset += im.size[0]

comb_Dis.save(Folder + '/Combined_Distribution.png')




