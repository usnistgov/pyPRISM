#!python
from __future__ import division,print_function
from typyPRISM.omega.Omega import Omega
from typyPRISM.omega.FreelyJointedChain import FreelyJointedChain
import numpy as np
import scipy.integrate 
import warnings

class NonOverlappingFreelyJointedChain(Omega):
    '''Freely jointed chain with excluded volume intra-molecular correlation function

    .. warning:: 
        This function is a work in
    
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
        
    def __repr__(self):
        return '<Omega: NonOverlappingFreelyJointedChain>'
    
    def calculate(self,k):
        integrate = np.trapz
        integrate = scipy.integrate.simps
        self.value = np.zeros_like(k)

        B = []
        dx = 0.01
        x = np.arange(dx,100,dx)
        K,X = np.meshgrid(k,x,indexing='ij')
        ZBase = (1/(np.pi*K))*X*(np.sin(K-X)/(K-X) - np.sin(K+X)/(K+X))
        for tau in range(2,self.length):
            J0val = 2/np.pi * integrate((np.sin(x)/x)**(tau) * (np.sin(x)/x - np.cos(x)),x=x)
            B = (1 - J0val)**(-1.0)
            Z = ZBase * (np.sin(X)/X)**(tau) 
            Jvals = integrate(Z,x=x,axis=1)
            omega_t = B * ((np.sin(k)/k)**(tau) - Jvals)
            self.value +=  (self.length - tau) * (omega_t - (np.sin(k)/k)**(tau))

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
        
        
