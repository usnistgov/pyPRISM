from __future__ import division,print_function
from pyPRISM.potential.Potential import Potential
import numpy as np

class OZExponential(Potential):
    
    def __init__(self,epsilon,alpha,sigma=None,high_value=1e6):
 
        self.epsilon1 = epsilon
        self.sigma = sigma
        self.alpha = alpha
        self.high_value = high_value
        self.funk  = lambda r,sigma: -(1/r) * (epsilon * np.exp(-(r-sigma)/(alpha))) 
        
    def __repr__(self):
        return '<Potential: AvanishOZExponential>'
    
    def calculate(self,r):
        assert (self.sigma is not None), 'Sigma must be set before evaluating potential!'

        magnitude = self.funk(r,self.sigma)
        magnitude = np.where(r>self.sigma,magnitude,self.high_value)
        return magnitude  