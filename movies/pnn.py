# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 20:17:45 2016

@author: Anush
"""
import numpy as np

class PNN:
    def __init__(self,C,sigma,X_test,X,y):
        self.C = C
        self.sigma = sigma
        self.X_test = X_test
        self.X = X
        self.y = y
    
    def row_inds(self,k):
        return np.where(self.y==k)[0]
    
    def input_layer(self,k):
        return np.exp((self.X[self.row_inds(k),:].dot(self.X_test.T)-1)/(self.sigma**2))
    
    def hidden_layer(self,inp):
        return np.sum(inp,0)
    
    def predict(self):
        self.output= np.array([self.hidden_layer(self.input_layer(k)) for k in range(1,self.C+1)])
        self.preds =np.array([np.argmax(self.output,0)])
        return self.preds
    
"""
X = np.array([[0.8, 0.3, 0.6, 0.2],
             [0.7, 0.4, 0.6, 0.3],
             [0.8, 0.3, 0.6, 0.3],
             [0.8, 0.4, 0.6, 0.2],
             [0.8, 0.3, 0.5, 0.2],
             [0.9, 0.4, 0.7, 0.2],
             [0.7, 0.3, 0.5, 0.2],
             [0.7, 0.4, 0.5, 0.3]])

y = np.array([[1 for i in range(4)]+[2 for i in range(4)]]).T

x = np.array([[0.75, 0.32, 0.6, 0.21], 
              [0.75, 0.32, 0.6, 0.21],
[0.9, 0.4, 0.7, 0.2]])

p = PNN(2,.5,x,X,y)
print(p.row_inds(1))
print(X[p.row_inds(1),:])
print(p.row_inds(2))
print(X[p.row_inds(2),:])
print(p.input_layer(1))
print(p.input_layer(2))   
print(p.hidden_layer(p.input_layer(1)))
print(p.hidden_layer(p.input_layer(2)))
print(p.predict())
print(p.preds)"""