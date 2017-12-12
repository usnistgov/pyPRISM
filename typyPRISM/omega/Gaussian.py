#!python
from __future__ import division,print_function
from typyPRISM.omega.Omega import Omega
import numpy as np

class Gaussian(Omega):
    r'''Gaussian intra-molecular correlation function
    
    
    **Mathematical Definition**

    .. math::
    
        \hat{\omega}(k) = \frac{1 - E^2 - \frac{2E}{N} + \frac{2E^{N+1}}{N}}{(1-E)^2}

    .. math::
         
         E = exp(-k^2\sigma^2/6)


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
    Schweizer, K.S.; Curro, J.G.; Integral-Equation Theory of Polymer Melts -
    Intramolecular Structure, Local Order, and the Correlation Hole,
    Macromolecules, 1988, 21 (10), pp 3070, doi:10.1021/ma00188a027

    Rubinstein, M; Colby, R.H; Polymer Physics. 2003. Oxford University Press.

    Example
    -------
    .. code-block:: python

        import typyPRISM
        import numpy as np
        import matplotlib.pyplot as plt

        #calculate Fourier space domain and omega values
        domain = typyPRISM.domain(dr=0.1,length=1000)
        omega  = typyPRISM.omega.Gaussian(l=1.0,length=100)
        x = domain.k
        y = omega.calculate(x)

        #plot it!
        plt.plot(x,y)
        plt.gca().set_xscale("log", nonposx='clip')
        plt.gca().set_yscale("log", nonposy='clip')

        plt.show()

    
    '''
    def __init__(self,sigma,length):
        self.sigma = sigma
        self.length = length
        self.value = None
        
    def __repr__(self):
        return '<Omega: Gaussian>'
    
    def calculate(self,k):
        E = np.exp(-k*k*self.sigma*self.sigma/6.0)
        N = self.length
        self.value = (1 - E*E - 2*E/N + (2*E**(N+1))/N)/((1-E)**2.0)
        return self.value
        
        
