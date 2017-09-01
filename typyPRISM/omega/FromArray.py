#!python
from __future__ import division,print_function
from typyPRISM.omega.Omega import Omega
import numpy as np

class FromArray(Omega):
    '''Read *intra*-molecular correlations from a list or array
    
    This class reads the omega from a Python list or Numpy array.
    
    Attributes
    ----------
    omega: np.ndarray
        intra-molecular omega

    k: np.narray, *optional*
        domain of the array data. Will be checked against the system
        domain if provided
        
    '''
    def __init__(self,omega,k=None):
        self.value = np.array(omega)
        self.k = np.array(k)
        
    def __repr__(self):
        return '<Omega: FromArray>'
    
    def calculate(self,k):
        assert self.value.shape[0] == k.shape[0],'Size of array differs from supplied domain!'
        if self.k is not None:
            assert self.k.shape[0] == k.shape[0],'Array domain size differs from supplied domain!'
            assert np.allclose(self.k,k),'Array domain differs from supplied domain!'
        return self.value
        
        
