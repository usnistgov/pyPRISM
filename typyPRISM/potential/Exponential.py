#!python
from __future__ import division,print_function
from typyPRISM.potential.Potential import Potential
import numpy as np
class Exponential(Potential):
    '''Exponential attractive interactions
    
    Hooper, Schweizer, Macromolecules, 2006, 39, 15, 5133
    
    .. math::
    
        U(r>=\sigma) - \varepsilon exp(- (r-\sigma)/(\alpha))
        U(r<\sigma) = high_value
    
    
    Parameters
    ----------
    
    epsilon: float
        strength of attraction
        
    sigma: float
        Contact distance 
        
    alpha: float
        range of attraction
        
    high_value: float, *optional*
        Value of potential when overlapping
    
    
    '''
    def __init__(self,epsilon,sigma,alpha,high_value=1e6):
        self.epsilon = epsilon
        self.sigma = sigma
        self.alpha = alpha
        self.high_value = high_value
        self.funk  = lambda r: - epsilon * np.exp(-(r-sigma)/(alpha))
    def __repr__(self):
        return '<Potential: Exponential>'
    
    def calculate(self,r):
        magnitude = self.funk(r)
        magnitude = np.where(r>self.sigma,magnitude,self.high_value)
        return magnitude
        