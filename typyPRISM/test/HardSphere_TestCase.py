import unittest
from typyPRISM.potential.HardSphere import HardSphere
import numpy as np

class HardSphere_TestCase(unittest.TestCase):
    def test_create(self):
        '''Can we create a LennardJones potential?'''
        r = np.arange(0.75,3.5,0.05)
        sigma   = 1.05
        high_value = 1e5
        
        U1 = np.zeros_like(r)
        U1[r<sigma] = high_value
        
        U2 = HardSphere(sigma,high_value).calculate(r)
        np.testing.assert_array_almost_equal(U1,U2)
        
        