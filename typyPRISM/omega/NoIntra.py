#!python
from __future__ import division,print_function
from typyPRISM.omega.Omega import Omega
import numpy as np

class NoIntra(Omega):
    '''inter-molecule intra-molecular correlation function
    
    This is a convenience class for specifying the intra-molecular
    correlations between sites which are never in the same molecule.
    Because they have no *intra*-molecular correlation, this function
    returns zero at all wavenumber.
    
    '''
    def __repr__(self):
        return '<Omega: NoIntra>'
    
    def calculate(self,k):
        self.value = np.zeros_like(k)
        return self.value
        
        