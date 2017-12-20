#!python
from __future__ import division,print_function
import unittest
from pyPRISM.potential.Exponential import Exponential
import numpy as np

class Exponential_TestCase(unittest.TestCase):
    def test_create(self):
        '''Can we create a Exponential potential?'''
        r = np.arange(0.75,3.5,0.05)
        sigma   = 1.05
        epsilon = 0.25
        alpha = 0.25
        
        U1  =  -epsilon * np.exp(-(r-sigma)/(alpha))
        U1 = np.where(r>sigma,U1,1e6)
        
        U2 = Exponential(sigma=sigma,epsilon=epsilon,alpha=alpha).calculate(r)
        np.testing.assert_array_almost_equal(U1,U2)
        
        
