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
#		Tensorflow model validation:
#			varaiables can be subject to change to create/format model where required
#
# ------------------------------------------------------------------------------------------------


# Required libraries
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from numpy import mean
from numpy import std
from sklearn.datasets import make_regression
from sklearn.model_selection import RepeatedKFold
from keras.models import Sequential
from keras.layers import Dense
import keras
import tensorflow as tf
import shap
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
from sklearn.inspection import permutation_importance



## Training data reading and trimming
path = '1m_training_data_4genes.csv'
df = read_csv(path,sep="\t")[0:500000]


# split into input and output columns
# Input variables in X
X= df.drop(['Sel_1','Sel_2','Sel_3','Sel_4','Bottleneck'], axis = 1)

#  Output variables in Y
y = df.drop(['Diversity','Divergence','Start_Diversity','output_1','output_2','output_3','output_4','input_1','input_2','input_3','input_4'], axis = 1)

# ensure all data are floating point values
#X = X.astype('float32')


## Load model
model = tf.keras.models.load_model('Tensorflow_Model')


# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.005, random_state=42)

# Train the neural network on the training set
"""
# Evaluate the model performance on the testing set
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)

# Calculate the baseline performance
baseline = test_acc
"""
# Calculate the feature importance scores
scoring = ['r2', 'neg_mean_absolute_percentage_error', 'neg_mean_squared_error']
results = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42,scoring='neg_mean_squared_error')
importance = results.importances_mean

# Print the feature importance scores
for i,v in enumerate(importance):
    print('Feature %d: %.5f' % (i,v))

# Plot the feature importance chart
plt.bar([x for x in range(len(importance))], importance)
plt.show()




