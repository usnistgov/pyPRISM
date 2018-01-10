#!python
from __future__ import division,print_function
from pyPRISM.omega.GaussianRing import GaussianRing
import unittest
import numpy as np

class GaussianRing_TestCase(unittest.TestCase):
    def test_create(self):
        '''Can we create a GaussianRing Omega?'''
        k = np.arange(0.75,3.5,0.05)
        sigma = 1.0
        length = N = 100
        
        
        O1 = np.zeros_like(k)
        ss = sigma * sigma
        kk = k*k
        for i in range(length):
            j = 0
            O1 += np.exp(-ss*kk*abs(i-j)*(length-abs(i-j))/(6.0*length))
        
        G = GaussianRing(sigma,length)
        O2 = G.calculate(k)
        np.testing.assert_array_almost_equal(O1,O2)
        
        
