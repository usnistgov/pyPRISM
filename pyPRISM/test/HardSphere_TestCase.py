#!python
from __future__ import division,print_function
import unittest
from pyPRISM.potential.HardSphere import HardSphere
import numpy as np

class HardSphere_TestCase(unittest.TestCase):
    def test_create(self):
        '''Can we create a HardSphere potential?'''
        r = np.arange(0.75,3.5,0.05)
        sigma   = 1.05
        high_value = 1e5
        
        U1 = np.ones_like(r)*high_value
        U1[r>sigma] = 0.0
        
        U2 = HardSphere(sigma,high_value).calculate(r)
        np.testing.assert_array_almost_equal(U1,U2)
        
        
