#!python
from __future__ import division,print_function
from typyPRISM.omega.Omega import Omega
from typyPRISM.omega.FreelyJointedChain import FreelyJointedChain
import numpy as np

class NonOverlappingFreelyJointedChain(Omega):
    '''Freely jointed chain with excluded volume intra-molecular correlation function
    
    Schweizer, K.S.; Curro, J.G.; Macromolecules 1988, 21, 3082-3087
    
    Attributes
    ----------
    N: float
        number of monomers/sites in gaussian chain
        
    l: float
        bond length
    
    .. math::
    
        \omega(k) = \frac{1 - E^2 - 2E/N + 2E^(N+1)/N}{(1-E)^2}
         
         E = np.sin(k*l)/(k*l)
    '''
    def __init__(self,N,l):
        self.N = N
        self.l = l
        self.FJC = FreelyJointedChain(N,l)
        self.value = None
        
    def __repr__(self):
        return '<Omega: NonOverlappingFreelyJointedChain>'
    
    def calculate(self,k):
        sin = np.sin
        cos = np.cos
        
        self.value = self.FJC.calculate(k)
        J0 = lambda y,tau: 1 * (sin(y)/y)**(tau) * ( sin(y)/(y) - cos(y) )
        J1 = lambda y,k,tau: y * (sin(y)/y)**(tau) * ( sin(k-y)/(k-y) - sin(k+y)/(k+y) )
        
        
        y = np.arange(0.001,100,dtype=np.float) #above integrals converge for N>1000
        B_vals = []
        for tau in range(N):
            J0_val = 2/np.pi * np.trapz(J0(y,tau),x=y)
            B_vals.append((1 - J0_val)**(-1.0))
            
        for i in range(self.value.shape[0]):
            ki = k[i]
            print(i,ki)
            J1_postFac =  (sin(ki-y)/(ki-y) - sin(ki+y)/(ki+y) )
            J1_preFac  = y*(sin(y)/y)
            sinkk = sin(ki)/ki
            for tau in range(N):
                B = B_vals[tau]
                sinkktau = sinkk**tau
                J1_val = 1/(np.pi*ki) * np.trapz(J1_preFac**(tau) * J1_postFac,x=y)
                omega_t = B * (sinkktau- J1_val)
                self.value[i] += 2/N * (N - tau) * (omega_t - sinkktau)
            
        return self.value
        
        