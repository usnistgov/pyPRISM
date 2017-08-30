#!python
from __future__ import division,print_function
from typyPRISM.potential.Potential import Potential
import numpy as np
class HardSphere(Potential):
    '''Simple hard sphere potential
    
    .. math::
    
        U(r>\sigma)  = 0.0
        U(r<=\sigma) = high_value
    
    
    Parameters
    ----------
    sigma: float
        Contact distance 
    
    high_value: float, *optional*
        Value of potential when overlapping
    
    
    '''
    def __init__(self,sigma,high_value=1e6):
        self.sigma = sigma
        self.high_value = high_value
        self.funk  = lambda r: np.where(r>sigma,0.0,high_value)
    def __repr__(self):
        return '<Potential: HardSphere>'
    
    def calculate(self,r):
        magnitude = self.funk(r)
        return magnitude
        