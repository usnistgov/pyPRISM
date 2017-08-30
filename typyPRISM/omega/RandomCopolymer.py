#!python
from __future__ import division,print_function
from typyPRISM.omega.Omega import Omega
import numpy as np

class RandomCopolymer(Omega):
    '''Random copolymer intra-molecular correlation function
    
    Attributes
    ----------
    sigma: float
        contact distance between these sites (i.e. site diameter)
        
    length,N: float
        number of monomers/sites in gaussian chain
        
    fx,fy: float, range (0,1)
        monomer fractions of monomer 1 and monomer 2 (x and y)
    
    cross: bool, 
        Specify whether this is a cross term (XY; cross=True) or a
        non-cross term (XX,YY; cross=False)
    
    '''
    def __init__(self,sigma,fx,N,cross=False):
        self.cross = cross
        self.sigma = sigma
        self.N = self.length = sigma
        self.fx = fx
        self.fy = 1-fx
        self.value = None
        
    def __repr__(self):
        return '<Omega: RandomCopolymer>'
    
    def calculate(self,k):
        raise NotImplementedError()
        # s1 = np.sin(k*self.sigma)/(k*self.sigma)
        # self.value = 0
        # if self.cross:
        #     self.value += 1/(int)
        #     for tau in range(1,self.N+2):
        #         pass
        # 
        # 
        # self.value = (1 - E*E - 2*E/N + (2*E**(N+1))/N)/((1-E)**2.0)
        # return self.value
        
        