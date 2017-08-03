from typyPRISM.potential.Potential import Potential
import numpy as np
class LennardJones(Potential):
    '''12-6 Lennard-Jones potential
    
    .. math::
    
        U(r) = 4 * \epsilon * ((\sigma/r)^(12.0) - (\sigma/r)^(6.0))
    
    
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
    def __init__(self,epsilon,sigma,rcut=None,shift=False):
        self.epsilon = epsilon
        self.sigma = sigma
        self.rcut  = rcut
        self.shift = shift
        self.funk  = lambda r: 4 * epsilon * ((sigma/r)**(12.0) - (sigma/r)**(6.0))
        
    def __repr__(self):
        return '<Potential: LennardJones>'
        
    def calculate(self,r):
        magnitude = self.funk(r)
        
        if self.rcut is not None:
            if self.shift:
                magnitude -= self.funk(self.rcut)
            magnitude[r>self.rcut] = 0.0
                
        return magnitude
        