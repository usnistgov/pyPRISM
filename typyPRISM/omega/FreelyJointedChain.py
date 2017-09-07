#!python
from __future__ import division,print_function
from typyPRISM.omega.Omega import Omega
import numpy as np


class FreelyJointedChain(Omega):
    '''Freely jointed chain intra-molecular correlation function
    
    Attributes
    ----------
    length,N: float
        number of monomers/sites in gaussian chain
        
    l: float
        bond length
    
    .. math::
    
        \omega(k) = \frac{1 - E^2 - 2E/N + 2E^(N+1)/N}{(1-E)^2}
         
         E = np.sin(k*l)/(k*l)
    '''
    def __init__(self,length,l):
        self.length = self.N = length
        self.l = l
        self.value = None
        
    def __repr__(self):
        return '<Omega: FreelyJointedChain>'
    
    def calculate(self,k):
        E = np.sin(k*self.l)/(k*self.l)
        N = self.N
        self.value = (1 - E*E - 2*E/N + (2*E**(N+1))/N)/((1-E)**2.0)
        return self.value
        
        
class FJC(FreelyJointedChain):
    '''Alias of FreelyJointedChain'''
    pass
