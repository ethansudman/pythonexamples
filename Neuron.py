#!/usr/bin/python

import random
import math

class Neuron:

	def __init__(self, num_inputs):
    		self.weights = []
    		for i in range(0, num_inputs):
    			self.weights.append(random.uniform(-2.4/num_inputs, 2.4/num_inputs))
    		self.threshold = random.uniform(-2.4/num_inputs, 2.4/num_inputs)
    		self.output = 0
    		self.learning_rate = .1
    		
    	def calculateOutput(self, inputs):
    		sum = 0
    		#My representation of the sigmoid function may not be correct...
    		for i in range(0, len(inputs)):
    			sum += inputs[i] * self.weights[i]
    		sum -= self.threshold
    		self.output = 1.0/(1.0 + math.exp(-sum))
    		self.inputs = inputs[:]
    		
    	def adjustWeights(self):
    		for i in range(0, len(self.inputs)):
    			self.weights[i] += self.learning_rate * self.inputs[i] * self.error
