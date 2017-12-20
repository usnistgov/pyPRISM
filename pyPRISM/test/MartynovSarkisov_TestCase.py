#!python
from __future__ import division,print_function
from pyPRISM.closure import MartynovSarkisov
import unittest
import numpy as np

class MartynovSarkisov_TestCase(unittest.TestCase):
    def test_create_hard_core(self):
        '''Can we create and use a hard-core MartynovSarkisov closure?'''
        r = np.arange(0.75,3.5,0.05)
        U = np.zeros_like(r)
        U[r<1.0] = 1e6
        sigma = 1.0
        
        gamma = np.zeros_like(r)
        C1 = -1 - gamma
        mask = r>sigma
        C1[mask] = np.exp(np.sqrt(gamma[mask] - U[mask] + 0.5) - 1.0) - 1.0 - gamma[mask]


        MS = MartynovSarkisov(apply_hard_core=True)
        MS.potential = U
        MS.sigma = sigma
        C2 = MS.calculate(r,gamma)
        np.testing.assert_array_almost_equal(C1,C2)
        
        
if __name__ == '__main__':
    import unittest 
    suite = unittest.TestLoader().loadTestsFromTestCase(MartynovSarkisov_TestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
