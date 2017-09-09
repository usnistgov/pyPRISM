#!python
from __future__ import division,print_function
from typyPRISM.potential.Potential import Potential
import numpy as np
class HardCoreLennardJones(Potential):
    '''12-6 Lennard-Jones potential with Hard Core

    Unlike the classic LJ potential, the HCLJ potential has an infinitely
    hard core and can handle negative and positive epsilons, corresponding
    the attractive and repulsive interactions.

    .. warning:: 

        This potential uses a slightly different form than what is 
        implemented for the LJ potential in order to match the PRISM
        literature.  This means that the epsilon in the LJ and HCLJ
        potentials will not correspond to the same interactions strengths..
    
    .. math::
    
        U(r>sigma) = \epsilon * ((\sigma/r)^(12.0) - (\sigma/r)^(6.0))
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
        self.epsilon = epsilon 
        self.sigma = sigma
        self.high_value = high_value
        self.funk  = lambda r: epsilon * ((sigma/r)**(12.0) - 2.0*(sigma/r)**(6.0))
        
    def __repr__(self):
        return '<Potential: HardCoreLennardJones>'
        
    def calculate(self,r):
        magnitude = self.funk(r)
        magnitude[r<=self.sigma] = self.high_value
                
        return magnitude
        
