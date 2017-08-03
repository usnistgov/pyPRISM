from typyPRISM.closure import PercusYevick
import unittest
import numpy as np

class PercusYevick_TestCase(unittest.TestCase):
    def test_create(self):
        '''Can we create a PercusYevick closure ?'''
        r = np.arange(0.75,3.5,0.05)
        U = np.zeros_like(r)
        U[r<1.0] = 1e6
        
        gamma = np.zeros_like(r)
        C1 = (np.exp(-U) - 1.0)*(1.0 + gamma)
        
        
        PY = PercusYevick()
        PY.potential = U
        C2 = PY.calculate(gamma)
        np.testing.assert_array_almost_equal(C1,C2)
        
        