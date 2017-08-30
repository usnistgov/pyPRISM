#!python
from __future__ import division,print_function
from typyPRISM.potential.LennardJones import LennardJones
import numpy as np
class HardCoreLennardJones(LennardJones):
    '''12-6 Lennard-Jones potential with Hard Core
    
    .. math::
    
        U(r>sigma) = 4 * \epsilon * ((\sigma/r)^(12.0) - (\sigma/r)^(6.0))
        U(r<=sigma) = inf
    
    
    Parameters
    ----------
    epsilon: float
        Depth of attractive well
        
    sigma: float
        Contact distance (i.e. low distance where potential magnitude = 0)
    
    rcut: float, *optional*
        Cutoff distance for potential. Useful for comparing directly to results
        from simulations where cutoffs are necessary. 
    
    shift: bool,*optional*
        Shift the potential by its value at the cutoff. Clearly this only makes 
        sense if rcut is specified
    
    '''
    def __init__(self,epsilon,sigma,high_value=1e6):
        super().__init__(epsilon=epsilon,sigma=sigma,rcut=None,shift=False)
        self.high_value = high_value
        
    def __repr__(self):
        return '<Potential: HardCoreLennardJones>'
        
    def calculate(self,r):
        magnitude = self.funk(r)
        magnitude[r<=self.sigma] = self.high_value
                
        return magnitude
        