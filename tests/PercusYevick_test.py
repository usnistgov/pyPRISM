#!python
from __future__ import division,print_function
from pyPRISM.closure import PercusYevick
import unittest
import numpy as np

class PercusYevick_TestCase(unittest.TestCase):
    def test_create(self):
        '''Can we create and use a PercusYevick closure?'''
        r = np.arange(0.75,3.5,0.05)
        U = np.zeros_like(r)
        U[r<1.0] = 1e6
        
        gamma = np.zeros_like(r)
        C1 = (np.exp(-U) - 1.0)*(1.0 + gamma)
        
        
        PY = PercusYevick(apply_hard_core=False)
        PY.potential = U
        PY.sigma = 1.0
        C2 = PY.calculate(r,gamma)
        np.testing.assert_array_almost_equal(C1,C2)
    def test_create_hard_core(self):
        '''Can we create and use a hard-core PercusYevick closure?'''
        r = np.arange(0.75,3.5,0.05)
        U = np.zeros_like(r)
        U[r<1.0] = 1e6
        sigma = 1.0
        
        gamma = np.zeros_like(r)
        C1 = -1 - gamma
        mask = r>sigma
        C1[mask] = (np.exp(-U[mask]) - 1.0)*(1.0 + gamma[mask])


        PY = PercusYevick(apply_hard_core=True)
        PY.potential = U
        PY.sigma = sigma
        C2 = PY.calculate(r,gamma)
        np.testing.assert_array_almost_equal(C1,C2)
        
        
if __name__ == '__main__':
    import unittest 
    suite = unittest.TestLoader().loadTestsFromTestCase(PercusYevick_TestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
