#!python
from __future__ import division,print_function
from pyPRISM.omega.Omega import Omega
import numpy as np

class GaussianRing(Omega):
    r'''Gaussian ring polymer intra-molecular correlation function
    
    
    **Mathematical Definition**

    .. math::
    
        \hat{\omega}(k) = 1+2N^{-1}\sum_{t=1}^{N-1}(N-t)\exp(\frac{-k^2\sigma^2t(N-t)}{6N})
         

    **Variable Definitions**

        - :math:`\hat{\omega}(k)` 
            *intra*-molecular correlation function at wavenumber :math:`k`

        - :math:`N`
            number of monomers/sites in gaussian ring
 
        - :math:`\sigma`
            contact distance between sites (i.e. site diameter)


    **Description**
        
    The Gaussian ring is an ideal model for a cyclic chain
    that assumes a random walk between successive monomer
    segments along the chain, constrained such that ends join
    together to form a ring with no intra-molecular excluded
    volume.


    References
    ----------
    Schweizer, K.S.; Curro, J.G.; Integral-Equation Theory of Polymer Melts -
    Intramolecular Structure, Local Order, and the Correlation Hole,
    Macromolecules, 1988, 21 (10), pp 3070, doi:10.1021/ma00188a027

    Example
    -------
    .. code-block:: python

        import pyPRISM
        import numpy as np
        import matplotlib.pyplot as plt

        #calculate Fourier space domain and omega values
        domain = pyPRISM.domain(dr=0.1,length=1000)
        omega  = pyPRISM.omega.GaussianRing(sigma=1.0,length=100)
        x = domain.k
        y = omega.calculate(x)

        #plot it!
        plt.plot(x,y)
        plt.gca().set_xscale("log", nonposx='clip')
        plt.gca().set_yscale("log", nonposy='clip')

        plt.show()

        #Define a PRISM system and set omega(k) for type A
        sys = pyPRISM.System(['A','B'],kT=1.0)
        sys.domain = pyPRISM.Domain(dr=0.1,length=1024)
        sys.omega['A','A']  = pyPRISM.omega.GaussianRing(sigma=1.0,length=100)

    
    '''
    def __init__(self,sigma,length):
        r'''Constructor
        
        Arguments
        ---------
        sigma: float
            contact distance between sites (site diameter)        
    
        length: float
            number of monomers/sites in gaussian ring
        '''
        self.sigma = sigma
        self.length = length
        self.value = None
        
    def __repr__(self):
        return '<Omega: GaussianRing>'
    
    def calculate(self,k):
        '''Return value of :math:`\hat{\omega}` at supplied :math:`k`

        Arguments
        ---------
        k: np.ndarray
            array of wavenumber values to calculate :math:`\omega` at
        
        '''
        self.value = np.zeros_like(k)
        ss = self.sigma * self.sigma
        kk = k*k
        for i in range(self.length):
            # for j in range(self.length):
            j = 0
            self.value += np.exp(-ss*kk*abs(i-j)*(self.length-abs(i-j))/(6.0*self.length))
        return self.value
        
        
