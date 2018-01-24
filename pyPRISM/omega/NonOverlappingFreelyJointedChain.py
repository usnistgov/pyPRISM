#!python
from __future__ import division,print_function
from pyPRISM.omega.Omega import Omega
from pyPRISM.omega.FreelyJointedChain import FreelyJointedChain
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

    .. math::
    
        \hat{\omega}(k) = \hat{\omega}_{id}(k)+\frac{2}{N}\sum_{\tau=2}^{N-1}(N-\tau)
			[\hat{\omega}_{\tau}(k)-(\sin(k)/k)^{\tau}]
    
    .. math::
    
        \tau = |\alpha-\beta| 


    **Variable Definitions**

        - :math:`\hat{\omega}(k)` 
            *intra*-molecular correlation function at wavenumber :math:`k`

        - :math:`\hat{\omega}_{id}(k)` 
            *intra*-molecular correlation function for the ideal freely-jointed 
	    chain at wavenumber :math:`k`. Please see equation (15)
	    of Reference [1] for the mathematical representation.
        
        - :math:`\hat{\omega}_{\tau}(k)` 
            Please see equations (17,18,21) of Reference [1] for the
            mathematical representation.
	
	- :math:`N`
            number of repeat units in chain
 
        - :math:`\tau`
            number of monomers along chain separating sites :math:`\alpha` 
	    and :math:`\beta`. 


    **Description**
        
        The non-overlapping freely-jointed chain is an adjustment to the ideal
        freely jointed chain model that includes the effects of the excluded
        volume of monomer segments (i.e. bonds are not free to rotate over all
        angles). This model assumes a constant bond length :math:`l`. 


    References
    ----------
    #. Schweizer, K.S.; Curro, J.G.; Integral-Equation Theory of Polymer Melts
       - Intramolecular Structure, Local Order, and the Correlation Hole,
       Macromolecules, 1988, 21 (10), pp 3070
       [`link <https://doi.org/10.1021/ma00188a027>`__]

    Example
    -------
    .. code-block:: python

        import pyPRISM
        import numpy as np
        import matplotlib.pyplot as plt

        #calculate Fourier space domain and omega values
        domain = pyPRISM.domain(dr=0.1,length=1000)
        omega  = pyPRISM.omega.NonOverlappingFreelyJointedChain(length=100,l=1.0)
        x = domain.k
        y = omega.calculate(x)

        #plot using matplotlib
        plt.plot(x,y)
        plt.gca().set_xscale("log", nonposx='clip')
        plt.gca().set_yscale("log", nonposy='clip')

        plt.show()
	
	#define a PRISM system and set omega(k) for type A
	sys = pyPRISM.System(['A','B'],kT=1.0)
	sys.domain = pyPRISM.Domain(dr=0.1,length=1024)
        sys.omega['A','A']  = pyPRISM.omega.NonOverlappingFreelyJointedChain(length=100,l=1.0)

    
    '''
    def __init__(self,length,l):
        r'''Constructor
        
        Arguments
        ---------
        length: float
            number of monomers/sites in non-overlapping freely-jointed chain
            
        l: float
            bond length
        '''
        self.length = self.N = length
        self.l = l
        self.FJC = FreelyJointedChain(length=length,l=l)
        self.value = None

        warnings.warn(NFJC_WARNING)
        
    def __repr__(self):
        return '<Omega: NonOverlappingFreelyJointedChain>'
    
    def calculate(self,k):
        '''Return value of :math:`\hat{\omega}` at supplied :math:`k`

        Arguments
        ---------
        k: np.ndarray
            array of wavenumber values to calculate :math:`\omega` at
        
        '''
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

class NFJC(NonOverlappingFreelyJointedChain):
    ''' Alias of NonOverlappingFreelyJointedChain '''
    pass
        
        
