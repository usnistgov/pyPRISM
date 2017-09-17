#!python
from __future__ import division,print_function
from typyPRISM.closure.AtomicClosure import AtomicClosure
import numpy as np
class PercusYevick(AtomicClosure):
    '''Percus Yevick closure evaluated in terms of a change of variables

    The Percus-Yevick (PY) is derived by expanding the exponential of the 
    direct correlation function, c, in powers of density shift from a 
    refence state. See Hansen and McDonald for a full derivation.
    
    The change of variables is necessary in order to use potentials with
    hard cores in the computational setting. Written in the standard form, 
    this closure diverges with divergent potentials, which makes it impossible 
    to numerically solve. 

    This closure has been shown to be accurate for systems with hard cores 
    (strongly repulsive at short distances) and when the potential is short
    ranged. 
    
    .. math::
        
        c(r) = (exp(-u(r)) - 1.0) * (1.0 + \gamma(r))
        
        \gamma(r) =  h(r) - c(r)

        h: Total correlation function
        c: Direct correlation function
        u: Interaction potential
        r: pair separation distance

    .. references::

        Hansen, J.P.; McDonald, I.R.; Theory of Simple Liquids; Chapter 4, 
		Section 4; 4th Edition (2013), Elsevier


    
    '''
    def __init__(self):
        self.potential = None
        self.value = None
        
    def __repr__(self):
        return '<AtomicClosure: PercusYevick>'
    
    def calculate(self,gamma):
        
        assert self.potential is not None,'Potential for this closure is not set!'
        
        assert len(gamma) == len(self.potential),'Domain mismatch!'
        
        self.value = (np.exp(-self.potential)-1.0)*(1.0+gamma)
        
        return self.value
        
        
