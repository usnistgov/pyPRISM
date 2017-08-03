from typyPRISM.potential.LennardJones import LennardJones
import numpy as np
class WeeksChandlerAndersen(LennardJones):
    '''Purely repulsive Weeks-Chandler-Andersen potential
    
    .. math::
    
        U(r) = 4 * \epsilon * ((\sigma/r)^(12.0) - (\sigma/r)^(6.0)) + epsilon, r<rcut
        U(r) = 0.0, r>=rcut
        r_{cut} = 2^(1.0/6.0) * \sigma
    
    
    Parameters
    ----------
    epsilon: float
        Repulsive strength modifier
        
    sigma: float
        Contact distance 
    
    '''
    def __init__(self,epsilon,sigma):
        rcut = sigma * 2**(1.0/6.0)
        super().__init__(epsilon,sigma,rcut=rcut,shift=True)
        
    def __repr__(self):
        return '<Potential: WeeksChandlerAndersen>'
        
        