"""
This script takes our doc2vec input and trains a neural network using TensorFlow and Keras.
"""

import tensorflow as tf
from tensorflow import keras

import numpy as np
import matplotlib.pyplot as plt

NUM_EPOCHS = 5

"""
	This function reads in our doc2vec input from some file, parses it, cleans it,
	and returns it as training data (observations and labels) and testing data
	(observations and labels).

	Args:
		None

	Returns:
		train_obs: Training observations (x-values)
		train_labels: Training labels (y-values)
		test_obs: Test observations (x-values)
		test_labels: Test labels (y-values)
"""
def get_data():
	# TODO: implement
	# TODO: clean/preprocess data, if necessary
	return train_obs, train_labels, test_obs, test_labels


"""
	This function initializes the model. Currently it is initialized with two layers,
	a dense ReLU layer follwed by a dense SoftMax layer, but we can add/modify layers
	as necessary.

	Args:
		None

	Returns:
		Keras model with specified form and layers (keras model object)
"""
def build_model():
	model = keras.Sequential([
		keras.layers.Dense(128, activation=tf.nn.relu),
		keras.layers.Dense(10, activation=tf.nn.softmax)
	])
	return model


"""
	This function adds settings to the model. Currently we add the optimizer, loss
	function, and metrics. Current settings are from an example, but we can use, e.g.,
	'sgd' for optimizer, 'mean_squared_error' for loss.

	Args:
		None

	Returns:
		Keras model settings to be used in compile
		-optimizer (update instructions)
		-loss (loss function)
		-metrics (see keras.io/metrics)
"""
def get_compile_settings():
	# The following are examples from the tutorial. TODO: replace with desired values
	optimizer = 'adam'
	loss = 'sparse_categorical_crossentropy'
	metrics = ['accuracy']
	return optimizer, loss, metrics

"""
	This function trains the given model using the given training data.

	Args:
		train_obs: Training observations (x-values)
		train_labels: Training labels (y-values)
		model: the model to train (keras model object)

	Returns:
		Trained keras model (keras model object)
"""
def train_model(train_obs, train_labels, model):
	my_optimizer, my_loss, my_metrics = get_compile_settings()
	model.compile(optimizer=my_optimizer, loss=my_loss, metrics=my_metrics)
	model.fit(train_obs, train_labels, epochs=NUM_EPOCHS)
	return model


"""
	This function tests the given model using the given test data, and prints
	the accuracy.

	Args:
		test_obs: Test observations (x-values)
		test_labels: Test labels (y-values)
		model: the trained model to test (keras model object)

	Returns:
		The accuracy of the model based on the test data
"""
def test_model(test_obs, test_labels, model):
	test_loss, test_acc = model.evaluate(test_obs, test_labels)
	print("Test accuracy:", test_acc)
	return test_acc


if __name__ == '__main__':
	train_obs, train_labels, test_obs, test_labels = get_data()
	model = build_model()
	model = train_model(train_obs, train_labels, model)
	model_acc = test_model(test_obs, test_labels, model)
	# TODO: wrap in loop, add arguments to tune different models
	# TODO: make predictions?