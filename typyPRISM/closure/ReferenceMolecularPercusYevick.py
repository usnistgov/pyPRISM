#!python
from __future__ import division,print_function
from typyPRISM.closure.MolecularClosure import MolecularClosure
from typyPRISM.closure.PercusYevick import PercusYevick

from scipy.signal import fftconvolve
import numpy as np

class ReferenceMolecularPercusYevick(MolecularClosure):
    '''Reference Molecular Percus Yevick (R-MPY) closure
    
    .. note::

        Schweizer, K.S.; Yethiraj, Arun; Polymer reference interaction site 
        model theory: New molecular closure for phase separating fluids and
        alloys, The Journal of Chemical Physics 98, 9053 (1993); 
        doi: 10.1063/1.464465

    Attributes
    ----------
    C0: np.ndarray
        Reference direct correlation function
    
    
    '''
    def __init__(self,C0):
        raise NotImplementedError('Molecular closures are untested and not fully implemented.')

        self._potential = None
        self.value = None
        self.PY = PercusYevick()
        self.C0 = C0
        
    def __repr__(self):
        return '<MolecularClosure: ReferenceMolecularPercusYevick>'


    @property
    def potential(self):
        return self._potential

    @potential.setter
    def potential(self,value):
        self._potential =  value
        self.PY.potential = value
    
    def calculate(self,gamma,omega1,omega2):
        
        assert self.potential is not None,'Potential for this closure is not set!'
        
        assert len(gamma) == len(self.potential),'Domain mismatch!'

        
        value = self.C0 + self.PY.calculate(gamma)

        self.value = fftconvolve(fftconvolve(omega1,value,mode='same'),omega2,mode='same')
        
        return self.value
