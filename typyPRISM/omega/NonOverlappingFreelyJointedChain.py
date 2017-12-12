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
    r'''Freely jointed chain with excluded volume intra-molecular correlation function


    .. warning:: 
        The numerical integrations required for the NFJC omega
        calculation are slow and scale poorly with chain length 
        so this omega may take minutes or longer to calculate 
        even for modest chain lengths e.g. N=200.

    
    **Mathematical Definition**

        See reference cited below for the mathematical representation
        of the non-overlapping freely jointed chain :math:`\hat{\omega}(k)`.

    **Description**
        
        The non-overlapping freely-jointed chain is an adjustment to the ideal
        freely jointed chain model that includes the effects of the excluded
        volume of monomer segments (i.e. bonds are not free to rotate over all
        angles). This model assumes a constant bond length :math:`l`. 


    References
    ----------
    Schweizer, K.S.; Curro, J.G.; Integral-Equation Theory of Polymer Melts -
    Intramolecular Structure, Local Order, and the Correlation Hole,
    Macromolecules, 1988, 21 (10), pp 3070, doi:10.1021/ma00188a027

    Example
    -------
    .. code-block:: python

        import typyPRISM
        import numpy as np
        import matplotlib.pyplot as plt

        #calculate Fourier space domain and omega values
        domain = typyPRISM.domain(dr=0.1,length=1000)
        omega  = typyPRISM.omega.NonOverlappingFreelyJointedChain(l=1.0,length=100)
        x = domain.k
        y = omega.calculate(x)

        #plot it!
        plt.plot(x,y)
        plt.gca().set_xscale("log", nonposx='clip')
        plt.gca().set_yscale("log", nonposy='clip')

        plt.show()

    
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
        
        
