#!python
from __future__ import division,print_function
from typyPRISM.closure.MolecularClosure import MolecularClosure
from typyPRISM.closure.PercusYevick import PercusYevick
from scipy.signal import fftconvolve
import numpy as np
class MolecularPercusYevick(MolecularClosure):
    '''Molecular Percus Yevick closure written in terms of a change of variables
    
    .. note::
    
        The change of variables is necessary in order to use potentials with
        hard cores. Written in the standard form, this closure diverges with
        divergent potentials, which makes it impossible to numerically solve. 
    
    .. math::
        
        c_{i,j}(r) = \omega(r) \star (exp(-U_{i,j}(r)) - 1.0) * (1.0 + \gamma_{i,j}(r)) \star \omega(r) \star
        
        \gamma_{i,j}(r) =  h_{i,j}(r) - c_{i,j}(r)
    
    '''
    def __init__(self):
        self._potential = None
        self.value = None
        self.atomic_closure = PercusYevick()
        
    @property
    def potential(self):
        return self._potential
    
    @potential.setter
    def potential(self,value):
        self._potential = value
        self.atomic_closure.potential = value
        
    def __repr__(self):
        return '<MolecularClosure: PercusYevick>'
    
    def calculate(self,gamma,omega1,omega2):
        
        assert self.potential is not None,'Potential for this closure is not set!'
        
        assert len(gamma) == len(self.potential),'Domain mismatch!'
        
        atomic_value = self.atomic_closure.calculate(gamma)
        
        # self.value = fftconvolve(fftconvolve(omega1,atomic_value,mode='same'),omega2,mode='same')
        self.value = np.convolve(np.convolve(omega1,atomic_value,mode='same'),omega2,mode='same')
        
        return self.value
        
        