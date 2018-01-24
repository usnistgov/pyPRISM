#!python
from __future__ import division,print_function
from pyPRISM.omega.Omega import Omega
import numpy as np

class Gaussian(Omega):
    r'''Gaussian intra-molecular correlation function
    
    
    **Mathematical Definition**

    .. math::
    
        \hat{\omega}(k) = \frac{1 - E^2 - \frac{2E}{N} + \frac{2E^{N+1}}{N}}{(1-E)^2}

    .. math::
         
         E = \exp(-k^2\sigma^2/6)


    **Variable Definitions**

        - :math:`\hat{\omega}(k)` 
            *intra*-molecular correlation function at wavenumber :math:`k`

        - :math:`N`
            number of monomers/sites in gaussian chain
 
        - :math:`\sigma`
            contact distance between sites (i.e. site diameter)


    **Description**
        
        The Gaussian chain is an ideal polymer chain model
        that assumes a random walk between successive monomer
        segments along the chain with no intra-molecular excluded
        volume.


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
        omega  = pyPRISM.omega.Gaussian(sigma=1.0,length=100)
        x = domain.k
        y = omega.calculate(x)

        #plot using matplotlib
        plt.plot(x,y)
        plt.gca().set_xscale("log", nonposx='clip')
        plt.gca().set_yscale("log", nonposy='clip')

        plt.show()

        #Define a PRISM system and set omega(k) for type A
        sys = pyPRISM.System(['A','B'],kT=1.0)
        sys.domain = pyPRISM.Domain(dr=0.1,length=1024)
        sys.omega['A','A']  = pyPRISM.omega.Gaussian(sigma=1.0,length=100)

    
    '''
    def __init__(self,sigma,length):
        r'''Constructor
        
        Arguments
        ---------
        sigma: float
	    contact distance between sites (site diameter)        
    
        length: float
            number of monomers/sites in gaussian chain
        '''
        self.sigma = sigma
        self.length = length
        self.value = None
        
    def __repr__(self):
        return '<Omega: Gaussian>'
    
    def calculate(self,k):
        '''Return value of :math:`\hat{\omega}` at supplied :math:`k`

        Arguments
        ---------
        k: np.ndarray
            array of wavenumber values to calculate :math:`\omega` at
        
        '''
        E = np.exp(-k*k*self.sigma*self.sigma/6.0)
        N = self.length
        self.value = (1 - E*E - 2*E/N + (2*E**(N+1))/N)/((1-E)**2.0)
        return self.value
        
        
