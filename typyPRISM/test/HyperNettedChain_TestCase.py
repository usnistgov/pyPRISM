#!python
from __future__ import division,print_function
from typyPRISM.closure import HyperNettedChain
import unittest
import numpy as np

class HyperNettedChain_TestCase(unittest.TestCase):
    def test_create(self):
        '''Can we create a HyperHyperNettedChain closure ?'''
        r = np.arange(0.75,3.5,0.05)
        U = np.zeros_like(r)
        U[r<1.0] = 1e6
        
        gamma = np.zeros_like(r)
        C1 = np.exp(gamma-U) - 1.0 - gamma
        
        
        HNC = HyperNettedChain()
        HNC.potential = U
        C2 = HNC.calculate(gamma)
        np.testing.assert_array_almost_equal(C1,C2)
        
        