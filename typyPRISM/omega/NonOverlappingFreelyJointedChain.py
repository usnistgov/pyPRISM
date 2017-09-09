#!python
from __future__ import division,print_function
from typyPRISM.omega.Omega import Omega
from typyPRISM.omega.FreelyJointedChain import FreelyJointedChain
import numpy as np
import scipy.integrate 

import warnings

NFJC_WARNING = '''
The numerical integrations required for the NFJC omega
calculation are slow and scale poorly with chain length 
so this omega may take minutes or longer to calculate 
even for modest chain lengths e.g. N=200.'''

class NonOverlappingFreelyJointedChain(Omega):
    '''Freely jointed chain with excluded volume intra-molecular correlation function

    .. warning:: 
        This function is provided
    
    Attributes
    ----------
    length,N: float
        number of monomers/sites in gaussian chain
        
    l: float
        bond length
    
    '''
    def __init__(self,length,l):

        self.length = self.N = length
        self.l = l
        self.FJC = FreelyJointedChain(length=length,l=l)
        self.value = None

        warnings.warn(NFJC_WARNING)
        
    def __repr__(self):
        return '<Omega: NonOverlappingFreelyJointedChain>'
    
    def calculate(self,k):
        integrate = np.trapz
        integrate = scipy.integrate.simps
        self.value = np.zeros_like(k)

        B = []
        dx = 0.1
        x = np.arange(dx,100,dx)
        K,X = np.meshgrid(k,x,indexing='ij')
        # Precaculate factors for efficiency 
        ZBase = (1/(np.pi*K))*X*(np.sin(K-X)/(K-X) - np.sin(K+X)/(K+X))
        sinxx = np.sin(x)/x
        sinXX = np.sin(X)/X
        sinkk = np.sin(k)/k
        J0Base = (np.sin(x)/x - np.cos(x))
        for tau in range(2,self.length):
            J0val = 2/np.pi * integrate((sinxx)**(tau)*J0Base,x=x)
            B = (1 - J0val)**(-1.0)
            Z = ZBase * (sinXX)**(tau) 
            Jvals = integrate(Z,x=x,axis=1)
            omega_t = B * ((sinkk)**(tau) - Jvals)
            self.value +=  (self.length - tau) * (omega_t - (sinkk)**(tau))

        self.value  *= 2.0/self.length 
        self.value  += self.FJC.calculate(k)


        return self.value

    def calculate2(self,k):
        self.value = np.zeros_like(k)

        JFunk = lambda y,k,tau: (1/(np.pi*k))*((np.sin(k)/k)**(tau))*y*(np.sin(k-y)/(k-y) - np.sin(k+y)/(k+y))
        J0Funk = lambda y,tau: 2/np.pi * (np.sin(y)/y)**(tau) * (np.sin(y)/y - np.cos(y))
        Jvals = np.empty_like(k)
        for tau in range(2,self.length):
            print('tau=',tau)
            J0Val = scipy.integrate.quad(J0Funk,0,np.inf,args=(tau),limit=int(1e4))[0]
            B = (1-J0Val)**(-1.0)
            for i,kval in enumerate(k):
                Jvals[i] = scipy.integrate.quad(JFunk,0,np.inf,args=(kval,tau),limit=int(1e4))[0]
            omega_t = B * ((np.sin(k)/k)**(tau) - Jvals)
            self.value +=  (self.length - tau) * (omega_t - (np.sin(k)/k)**(tau))

        self.value  *= 2.0/self.length 
        self.value  += self.FJC.calculate(k)


        return self.value
class NFJC(NonOverlappingFreelyJointedChain):
    ''' Alias of NonOverlappingFreelyJointedChain '''
    pass
        
        
