#!python
from __future__ import division,print_function
import unittest
from pyPRISM.potential.LennardJones import LennardJones
import numpy as np

class LennardJones_TestCase(unittest.TestCase):
    def test_create(self):
        '''Can we create a LennardJones potential?'''
        r = np.arange(0.75,3.5,0.05)
        epsilon = 0.25
        sigma   = 1.05
        rcut    = 2.5*sigma
        shift   = True
        
        UShift = 4*epsilon*((sigma/rcut)**(12.0) - (sigma/rcut)**(6.0))
        U1 = 4*epsilon*((sigma/r)**(12.0) - (sigma/r)**(6.0)) - UShift
        U1[r>rcut] = 0
        
        U2 = LennardJones(epsilon,sigma,rcut=rcut,shift=shift).calculate(r)
        np.testing.assert_array_almost_equal(U1,U2)
        
        
