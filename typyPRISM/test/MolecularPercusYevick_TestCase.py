#!python
from __future__ import division,print_function
from typyPRISM.closure import MolecularPercusYevick
from scipy.signal import fftconvolve
import unittest
import numpy as np

class MolecularPercusYevick_TestCase(unittest.TestCase):
    def test_create(self):
        '''Can we create a MolecularPercusYevick closure ?'''
        r = np.arange(0.75,3.5,0.05)
        U = np.zeros_like(r)
        U[r<1.0] = 1e6
        
        omega = np.ones_like(r)
        
        gamma = np.zeros_like(r)
        C1 = (np.exp(-U) - 1.0)*(1.0 + gamma)
        
        C1 = fftconvolve(fftconvolve(omega,C1,mode='same'),omega,mode='same')
        
        
        PY = MolecularPercusYevick()
        PY.potential = U
        C2 = PY.calculate(gamma,omega,omega)
        np.testing.assert_array_almost_equal(C1,C2)
        
        