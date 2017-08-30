#!python
from __future__ import division,print_function
from typyPRISM.omega.Omega import Omega
import numpy as np

class Gaussian(Omega):
    '''Gaussian intra-molecular correlation function
    
    Attributes
    ----------
    sigma: float
        contact distance between these sites (i.e. site diameter)
        
    length,N: float
        number of monomers/sites in gaussian chain
    
    .. math::
    
        \omega(k) = \frac{1 - E^2 - 2E/N + 2E^(N+1)/N}{(1-E)^2}
         
         E = exp(-(k^2\sigma^2)/6)
    '''
    def __init__(self,sigma,length):
        self.sigma = sigma
        self.length = length
        self.value = None
        
    def __repr__(self):
        return '<Omega: Gaussian>'
    
    def calculate(self,k):
        E = np.exp(-k*k*self.sigma*self.sigma/6.0)
        N = self.length
        self.value = (1 - E*E - 2*E/N + (2*E**(N+1))/N)/((1-E)**2.0)
        return self.value
        
        