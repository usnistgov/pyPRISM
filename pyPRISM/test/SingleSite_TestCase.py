#!python
from __future__ import division,print_function
from pyPRISM.omega.SingleSite import SingleSite
import unittest
import numpy as np

class SingleSite_TestCase(unittest.TestCase):
    def test_create(self):
        '''Can we create a SingleSite Omega?'''
        k = np.arange(0.75,3.5,0.05)
        O1 = np.ones_like(k)
        
        O2 = SingleSite().calculate(k)
        np.testing.assert_array_almost_equal(O1,O2)
        
        
