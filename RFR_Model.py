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
#  		Random forest regression model generation
#		 Input variables subject to change
# 
#
# ------------------------------------------------------------------------------------------------


# Importing the libraries
import numpy as np # for array operations
import pandas as pd # for working with DataFrames
import requests, io # for HTTP requests and I/O commands
import matplotlib.pyplot as plt # for data visualization
import seaborn as sns

# scikit-learn modules
from sklearn.model_selection import train_test_split # for splitting the data
from sklearn.metrics import mean_squared_error # for calculating the cost function
from sklearn.ensemble import RandomForestRegressor # for building the model
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree

# Read training data
data = pd.read_csv('1m_training_data_4genes.csv',sep="\t")

# Split into input and output variables

# x holds input data
x = data.drop(['Bottleneck','Sel_1','Sel_2','Sel_3','Sel_4'], axis = 1)

# y holds output data
y = data['Bottleneck']  # Target

# Define number of input features for later weighting 
features = x.columns.values

## Scatter plot of input variables by output variable
g = sns.pairplot(data.head(100), hue='Bottleneck')
g.fig.suptitle("Scatterplot and histogram of pairs of variables color coded by risk level", 
               fontsize = 14, # defining the size of the title
               y=1.05); # y = defining title y position (height)


# Split data into test and training sets (0.3 = 30% test)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 28)


# Initializing the Random Forest Regression model with 10 decision trees
rfc = RandomForestRegressor(n_estimators=1000, max_depth=5,random_state=42)


# Fitting the Random Forest Regression model to the data
rfc.fit(x_train, y_train)

# Predict the test set labels
# In vivo example - this can be changed to other csv files or in silico data
in_vivo_data = pd.read_csv('joes_data_in_vivo.txt',sep="\t")
x_in_vivo = in_vivo_data.drop(['Time'], axis = 1)
y_pred = rfc.predict(x_in_vivo)


print("True_Value\tPredicted_Value")

for i in range(0,24):
	print(str(list(y_pred)[i]))



## Define importance of each input variable

features = x.columns.values # The name of each column

importances = list(rfc.feature_importances_)

feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(features, importances)]
# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
# Print out the feature and importances 
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];

# Plot importance of each variable
# Import tools needed for visualization
from sklearn.tree import export_graphviz
import pydot
# Pull out one tree from the forest
tree = rfc.estimators_[5]
# Export the image to a dot file
export_graphviz(tree, out_file = 'tree.dot', feature_names = features, rounded = True, precision = 1)
# Use dot file to create a graph
(graph, ) = pydot.graph_from_dot_file('tree.dot')
# Write graph to a png file
graph.write_png('tree.png')






