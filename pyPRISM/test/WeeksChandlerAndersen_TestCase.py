#!python
from __future__ import division,print_function
import unittest
from pyPRISM.potential.WeeksChandlerAndersen import WeeksChandlerAndersen
import numpy as np

class WeeksChandlerAndersen_TestCase(unittest.TestCase):
    def test_create(self):
        '''Can we create a WeeksChandlerAndersen potential?'''
        r = np.arange(0.75,3.5,0.05)
        epsilon = 0.25
        sigma   = 1.05
        rcut    = 2.0**(1.0/6.0)*sigma
        shift   = True
        
        UShift = 4*epsilon*((sigma/rcut)**(12.0) - (sigma/rcut)**(6.0))
        U1 = 4*epsilon*((sigma/r)**(12.0) - (sigma/r)**(6.0)) - UShift
        U1[r>rcut] = 0
        
        U2 = WeeksChandlerAndersen(epsilon,sigma).calculate(r)
        np.testing.assert_array_almost_equal(U1,U2)
        
        
