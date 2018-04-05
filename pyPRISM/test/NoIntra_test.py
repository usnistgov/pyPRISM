from pyPRISM.omega.NoIntra import NoIntra
import unittest
import numpy as np

class NoIntra_TestCase(unittest.TestCase):
    def test_create(self):
        '''Can we create a NoIntra Omega?'''
        k = np.arange(0.75,3.5,0.05)
        O1 = np.zeros_like(k)
        
        O2 = NoIntra().calculate(k)
        np.testing.assert_array_almost_equal(O1,O2)
        
        
