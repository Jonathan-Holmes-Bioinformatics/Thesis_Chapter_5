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
#		Tensorflow model creation:
#			varaiables can be subject to change to create/format model where required
#
# ------------------------------------------------------------------------------------------------


# Requried libraires
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

# Load training data and trim for time saving
path = '1m_training_data_4genes.csv'
df = read_csv(path,sep="\t")[0:500000]


# split into input and output columns
# Input variables in X
X= df.drop(['Sel_1','Sel_2','Sel_3','Sel_4','Bottleneck'], axis = 1)

#  Output variables in Y
y = df.drop(['Diversity','Divergence','Start_Diversity','output_1','output_2','output_3','output_4','input_1','input_2','input_3','input_4'], axis = 1)

# ensure all data are floating point values
#X = X.astype('float32')

# encode strings to integer

# split into train and test datasets

## Set up neural network architecture here
def get_model(n_inputs, n_outputs):
	model = Sequential()
	model.add(Dense(20, input_dim=n_inputs, kernel_initializer='he_uniform', activation='relu'))
	model.add(Dense(20, input_dim=n_inputs, kernel_initializer='he_uniform', activation='relu'))
	model.add(Dense(n_outputs))
	model.compile(loss='mae', optimizer='adam')
	return model

# evaluate a model using repeated k-fold cross-validation
def evaluate_model(X, y):
	results = list()
	n_inputs, n_outputs = X.shape[1], y.shape[1]
	# define evaluation procedure
	cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
	# enumerate folds
	for train_ix, test_ix in cv.split(X):
		# prepare data
		X_train, X_test = X[train_ix], X[test_ix]
		y_train, y_test = y[train_ix], y[test_ix]
		# define model
		model = get_model(n_inputs, n_outputs)
		# fit model
		model.fit(X_train, y_train, verbose=0, epochs=100)
		# evaluate model on test set
		mae = model.evaluate(X_test, y_test, verbose=0)
		# store result
		print('>%.3f' % mae)
		results.append(mae)
	return results


X = X.to_numpy()
y = y.to_numpy()

n_inputs, n_outputs = X.shape[1], y.shape[1]

results = evaluate_model(X, y)

print('MAE: %.3f (%.3f)' % (mean(results), std(results)))

# Get model - fit model (100 gens) - save model
model = get_model(n_inputs, n_outputs)
model.fit(X, y, verbose=0, epochs=100)
model.save("Tensorflow_Model")


## Run a section of the training data back into the model to test for function
yhat = model.predict(X[0:500])
p = 0

def to_string(A):
	B = []
	for i in A:
		B.append(str(i))
	return B


print(model.summary())


for i in range(0, len(yhat)):
	print("\t".join(to_string(y[i])) + "\t\t" + "\t".join(to_string(yhat[i])))
















