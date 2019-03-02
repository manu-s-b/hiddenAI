import math
import numpy as np
import random

class Hidden:
	def __init__(self,input_shape,output_shape):
		self.config = {"dimension":"ANY","type":"HIDDEN"}
		self.input_shape = input_shape if hasattr(input_shape,"__iter__") else [input_shape]
		self.output_shape = output_shape if hasattr(output_shape,"__iter__") else [output_shape]
	
	def run(self,input_layer): #may be over rided if the layer is 1d to 2d, or a different form
		pass# overided as they differ heavily

	def derivative(self, input_layer,output_layer_derivative):
		pass# to be overrided

	def derivative_prev_layer(self,input_layer, output_layer_derivative): # how does the previous layer affect the next
		pass# to be overrided
		
	def descend(self, derivatives): 
		self.weights -= derivatives
	
	def blank(self):
		pass # to be overided

	def __repr__(self):
		return str(self.weights)

		
class Bias(Hidden):#TESTED - while bias resembles an activation function as the size doesnt change, it does have variables so it is put in hidden
	def __init__(self,starting_values = "none"):
		self.starting_values = starting_values
		self.config = {"dimension":"ANY","type":"HIDDEN"}

	def init_input_shape(self,input_shape):
		super().__init__(input_shape,input_shape)
		self.weights = np.random.randn(*self.input_shape) 

	def compute_output_shape(self):
		return self.input_shape

	def run(self,input_layer):
		return input_layer + self.weights 

	def derivative(self,input_layer, output_layer_derivative):
		return output_layer_derivative

	def derivative_prev_layer(self,input_layer,output_layer_derivative): 
		return output_layer_derivative # the derivative of z= x+y for x is 1 and for y is 1 as well, so multiply it by the current derivative and its just current derivative 
	
	def blank(self):
		return np.zeros(self.input_shape)	

class FullyConnected(Hidden):#TESTED 
	def __init__(self, output_shape):
		self.config = {"dimension":1,"type":"HIDDEN"}
		self.output_shape = output_shape 
	
	def init_input_shape(self,input_shape):
		super().__init__(input_shape,self.output_shape)	
		self.weights = np.random.randn(self.output_shape[0],self.input_shape[0])	
		self.num_weights = self.input_shape[0]*self.output_shape[0]
	
	def compute_output_shape(self):
		return self.output_shape
	
	def run(self,input_layer):
		return np.matmul(self.weights,input_layer)
	
	def derivative(self,input_layer,output_layer_derivative):
		return np.array([[input_layer[x]*output_layer_derivative[y] for x in range(self.input_shape[0])] for y in range(self.output_shape[0])])
	
	def derivative_prev_layer(self,input_layer, output_layer_derivative): # we dont need an input layer for this derivative, but we keep it so all derivativePrevLayers can be called the same
		return np.matmul(np.swapaxes(self.weights,0,1),output_layer_derivative)

	def blank(self):
		return np.zeros((self.output_shape[0],self.input_shape[0]))
