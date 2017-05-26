from random import seed
from random import random

def initialize_network(n_inputs, n_hidden, n_outputs):
	network = list()

	hidden_layer = []
	for i in range(n_hidden):
		hidden_layer.append({'weights':[random() for i in range(n_inputs + 1)]})
	network.append(hidden_layer)
	output_layer = [{'weights':[random() for i in range(n_hidden + 1)]} for i in range(n_outputs)]
	network.append(output_layer)
	return network



seed(1)
network = initialize_network(3, 1, 2)
for layer in network:
	print(layer)