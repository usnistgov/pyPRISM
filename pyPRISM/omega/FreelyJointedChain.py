#!python
from __future__ import division,print_function
from pyPRISM.omega.Omega import Omega
import numpy as np


class FreelyJointedChain(Omega):
    r'''Freely jointed chain intra-molecular correlation function

    **Mathematical Definition**

    .. math::
    
        \hat{\omega}(k) = \frac{1 - E^2 - \frac{2E}{N} + \frac{2E^{N+1}}{N}}{(1-E)^2}

    .. math::
         
         E = \frac{\sin(k l)}{k l}


    **Variable Definitions**

        - :math:`\hat{\omega}(k)` 
            *intra*-molecular correlation function at wavenumber :math:`k`

        - :math:`N`
            number of repeat units in chain
 
        - :math:`l`
            bond-length


    **Description**
        
        The freely-jointed chain is an ideal polymer chain model
        that assumes a constant bond length :math:`l` and no correlations
        between the directions of different bond vectors 
        (i.e. :math:`<cos(\theta_{ij})>=0`). In other words, monomer segments
        are assumed to have no intra-molecular excluded volume.


    References
    ----------
    #. Schweizer, K.S.; Curro, J.G.; Integral-Equation Theory of Polymer Melts
       - Intramolecular Structure, Local Order, and the Correlation Hole,
       Macromolecules, 1988, 21 (10), pp 3070
       [`link <https://doi.org/10.1021/ma00188a027>`__]

    #. Rubinstein, M; Colby, R.H; Polymer Physics. 2003. Oxford University Press.

    Example
    -------
    .. code-block:: python

        import pyPRISM
        import numpy as np
        import matplotlib.pyplot as plt

        #calculate Fourier space domain and omega values
        domain = pyPRISM.domain(dr=0.1,length=1000)
        omega  = pyPRISM.omega.FreelyJointedChain(length=100,l=1.0)
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
        sys.omega['A','A']  = pyPRISM.omega.FreelyJointedChain(length=100,l=1.0)

    
    '''
    def __init__(self,length,l):
        r'''Constructor
        
        Arguments
        ---------
        length: float
            number of monomers/sites in Freely-jointed chain
            
        l: float
            bond length
        '''
        self.length = self.N = length
        self.l = l
        self.value = None
        
    def __repr__(self):
        return '<Omega: FreelyJointedChain>'
    
    def calculate(self,k):
        '''Return value of :math:`\hat{\omega}` at supplied :math:`k`

        Arguments
        ---------
        k: np.ndarray
            array of wavenumber values to calculate :math:`\omega` at
        
        '''
        E = np.sin(k*self.l)/(k*self.l)
        N = self.N
        self.value = (1 - E*E - 2*E/N + (2*E**(N+1))/N)/((1-E)**2.0)
        return self.value
        
        
class FJC(FreelyJointedChain):
    '''Alias of FreelyJointedChain'''
    pass
