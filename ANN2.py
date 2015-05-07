#!/usr/bin/python

import math
import random
import Neuron

#SEE http://www.codeproject.com/KB/cs/BackPropagationNeuralNet.aspx FOR POSSIBLE NEW SOLUTIONS

data = []
scaled_data = []
desired = []
#validate = []
num_data = 13
num_inputs = 13
num_outputs = 3
num_hiddens = int(2.0/3.0*num_inputs + num_outputs) #can change this -- one site suggested 2/3's of inputs plus outputs

infile = open("data.txt","r")
for line in infile.readlines():
	line_split = line.strip().split(",")
	desired.append(int(line_split[0]))
	data.append([float(s) for s in line_split[1:]])
infile.close()
t = zip(*data)
maxes = [reduce(max, row, 0.0) for row in t]
mins = [reduce(min, row, 10000.0) for row in t]
for line in data:
	scaled_data.append([(x-low)/(hi-low) for x, low, hi in zip(line, mins, maxes)])
#random.shuffle(scaled_data)
#for i in range(0, int(len(scaled_data)*.1)):
	#validate.append(scaled_data.pop())

input_layer = []
for i in range(0, num_inputs):
	input_layer.append(Neuron.Neuron(num_data))
hidden_layer = []
for j in range(0, num_hiddens):
	hidden_layer.append(Neuron.Neuron(num_inputs))
output_layer = []
for k in range(0, num_outputs):
	output_layer.append(Neuron.Neuron(num_hiddens))

for iteration in range(0,200):
        print "EPOCH ", iteration
	for d in range(0, len(scaled_data)):
		print "\n\n************************************";
		input_neuron_outputs = []
		hidden_neuron_outputs = []
		output_neuron_outputs = []
		desired_outputs = num_outputs*[0]
		desired_outputs[desired[d]-1]=1
		print "Yd: ", desired_outputs
		
		#calculate input layer output
		for input_neuron in input_layer:
			input_neuron.calculateOutput(scaled_data[d])
			input_neuron_outputs.append(input_neuron.output)
			
		#calculate hidden layer output
		for hidden_neuron in hidden_layer:
			hidden_neuron.calculateOutput(input_neuron_outputs)
			hidden_neuron_outputs.append(hidden_neuron.output)
			
		#calculate output layer output and error and adjust weights
		for k in range(0, num_outputs):
			output_layer[k].calculateOutput(hidden_neuron_outputs)
			output_neuron_outputs.append(output_layer[k].output)
			output_layer[k].error = output_layer[k].output * (1.0 - output_layer[k].output) * (desired_outputs[k] - output_layer[k].output)
			#output_layer[k].adjustWeights()
			print "KOut, KError: ", output_layer[k].output, output_layer[k].error
			
		#calculate hidden layer error and adjust weights
		for j in range(0, num_hiddens):
			sum = 0.0;
			for k in range(0, num_outputs):
				sum += output_layer[k].weights[j] * output_layer[k].error
			hidden_layer[j].error = sum
			#hidden_layer[j].adjustWeights()
			#print "JError: ", hidden_layer[j].error
			
		#calculate input layer error and adjust weights
		for i in range(0, num_inputs):
			sum = 0.0;
			for j in range(0, num_hiddens):
				sum += hidden_layer[j].weights[i] * hidden_layer[j].error
			input_layer[i].error = sum
			#input_layer[i].adjustWeights()
			#print "IError: ", input_layer[i].error
		for neuron in input_layer:
			neuron.adjustWeights()
		for neuron in hidden_layer:
			neuron.adjustWeights()
		for neuron in output_layer:
			neuron.adjustWeights()
