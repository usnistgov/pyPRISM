#!python
from __future__ import division,print_function
from typyPRISM.omega.Omega import Omega
import numpy as np

class Koyama(Omega):
    '''Semi-flexible Koyama-based intra-molecular correlation function

    .. note::
        Kevin G. Honnell, John G. Curro, Kenneth S. Schweizer
        Local structure of semiflexible polymer melts
        Macromolecules, 1990, 23 (14), pp 3496–3505
    
    Attributes
    ----------
    sigma: float
        contact distance between these sites (i.e. site diameter)

    lb: float
        bond length
        
    length: float
        number of monomers/sites in the chain

    lp: float
        persistence length
    '''
    def __init__(self,sigma,lb,length,lp):
        self.sigma = sigma
        self.length = length
        self.lb = lb
        self.lp = lp
        self.value = None
        
    def __repr__(self):
        return '<Omega: Koyama>'
    
    def calculate(self,k):
        cos =  1.0 - self.lb/self.lp
        th0 = np.arccos(1.0 - self.sigma*self.sigma/(2.0 * self.lb * self.lb))
        
        return self.value
        
        
