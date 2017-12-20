#!python
from __future__ import division,print_function
from pyPRISM.omega.Gaussian import Gaussian
import unittest
import numpy as np

class Gaussian_TestCase(unittest.TestCase):
    def test_create(self):
        '''Can we create a Gaussian Omega?'''
        k = np.arange(0.75,3.5,0.05)
        sigma = 1.0
        length = N = 100
        
        E = np.exp(-k*k*sigma*sigma/6.0)
        N = length
        O1 = (1 - E*E - 2*E/N + (2*E**(N+1))/N)/((1-E)**2.0)
        
        G = Gaussian(sigma,length)
        O2 = G.calculate(k)
        np.testing.assert_array_almost_equal(O1,O2)
        
        
