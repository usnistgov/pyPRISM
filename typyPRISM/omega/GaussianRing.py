#!python
from __future__ import division,print_function
from typyPRISM.omega.Omega import Omega
import numpy as np

class GaussianRing(Omega):
    '''Gaussian ring polymer intra-molecular correlation function
    
    Attributes
    ----------
    sigma: float
        contact distance between these sites (i.e. site diameter)
        
    length,N: float
        number of monomers/sites in gaussian chain
    
    '''
    def __init__(self,sigma,length):
        self.sigma = sigma
        self.length = length
        self.value = None
        
    def __repr__(self):
        return '<Omega: GaussianRing>'
    
    def calculate(self,k):
        self.value = np.zeros_like(k)
        ss = self.sigma * self.sigma
        kk = k*k
        for i in range(self.length):
            # for j in range(self.length):
            j = 0
            self.value += np.exp(-ss*kk*abs(i-j)*(self.length-abs(i-j))/(6.0*self.length))
        return self.value
        
        