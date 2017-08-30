#!python
from __future__ import division,print_function
from typyPRISM.omega.Omega import Omega
import numpy as np

class SingleSite(Omega):
    '''Single-site intra-molecular correlation function
    
    This class is useful for dealing with single bead molecules
    such as solvent or large particles. 
    
    '''
    def __repr__(self):
        return '<Omega: SingleSite>'
    
    def calculate(self,k):
        self.value = np.ones_like(k)
        return self.value
        
        