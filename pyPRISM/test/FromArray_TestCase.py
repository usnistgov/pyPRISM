#!python
from __future__ import division,print_function
from pyPRISM.omega.FromArray import FromArray
import unittest
import numpy as np
import os

class FromArray_TestCase(unittest.TestCase):
    def test_create(self):
        '''Can we create a FromArray Omega?'''
        k = np.arange(0.75,3.5,0.05)
        omega = np.ones_like(k)
        
        
        FF = FromArray(k=k,omega=omega).calculate(k)
        
    def test_error_check(self):
        '''Does FromFile correctly check the domain?'''
        fname = 'FromFileTestCase.dat'

        k1 = np.arange(0.75,3.5,0.05)
        k2 = np.arange(0.75,3.5,0.01)
        k3 = np.arange(0.75,4.0,0.05)
        omega = np.ones_like(k1)

        
        with self.assertRaises(AssertionError):
            FF = FromArray(k=k1,omega=omega).calculate(k2)

        with self.assertRaises(AssertionError):
            FF = FromArray(k=k1,omega=omega).calculate(k3)
        
        
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(FromArray_TestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
