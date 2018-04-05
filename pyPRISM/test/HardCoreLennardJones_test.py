#!python
from __future__ import division,print_function
import unittest
from pyPRISM.potential.HardCoreLennardJones import HardCoreLennardJones
import numpy as np

class HardCoreLennardJones_TestCase(unittest.TestCase):
    def test_create(self):
        '''Can we create a HardCoreLennardJones potential?'''
        r = np.arange(0.75,3.5,0.05)
        epsilon = 0.25
        sigma   = 1.05
        high_value = 1e6
        
        U1 = epsilon*((sigma/r)**(12.0) - 2*(sigma/r)**(6.0))
        U1[r<=sigma] = high_value
        
        U2 = HardCoreLennardJones(epsilon,sigma,high_value=high_value).calculate(r)
        np.testing.assert_array_almost_equal(U1,U2)
        
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(HardCoreLennardJones_TestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
