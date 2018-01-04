#!python
from __future__ import division,print_function
from pyPRISM.omega.FreelyJointedChain import FreelyJointedChain
import unittest
import numpy as np

class FreelyJointedChain_TestCase(unittest.TestCase):
    def test_create(self):
        '''Can we create a FreelyJointedChain Omega?'''
        k = np.arange(0.75,3.5,0.05)
        N = 100
        l = 4.0/3.0
        
        E = np.sin(k*l)/(k*l)
        N = N
        O1 = (1 - E*E - 2*E/N + (2*E**(N+1))/N)/((1-E)**2.0)
        
        G = FreelyJointedChain(N,l)
        O2 = G.calculate(k)
        np.testing.assert_array_almost_equal(O1,O2)
        
        
