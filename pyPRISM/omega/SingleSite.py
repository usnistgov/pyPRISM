#!python
from __future__ import division,print_function
from pyPRISM.omega.Omega import Omega
import numpy as np

class SingleSite(Omega):
    '''Single-site intra-molecular correlation function
    
    This class is useful for dealing with single bead molecules
    such as solvents or large spherical particles, it sets the value
    of the intra-molecular correlation function to 1 for all wavenumbers. 
    
    Example
    -------
    .. code-block:: python

        import pyPRISM
        import numpy as np

        #set omega(k) for type A to 1 (single spherical site per molecule)
	sys = pyPRISM.System(['A','B'],kT=1.0)
	sys.domain = pyPRISM.Domain(dr=0.1,length=1024)
	sys.omega['A','A']  = pyPRISM.omega.SingleSite()
        x = sys.domain.k
        y = sys.omega['A','A'].calculate(x)

        #plot using matplotlib
        plt.plot(x,y)
        plt.gca().set_xscale("log", nonposx='clip')
        plt.gca().set_yscale("log", nonposy='clip')

        plt.show()
    
    '''
    def __repr__(self):
        return '<Omega: SingleSite>'
    
    def calculate(self,k):
        '''Return value of :math:`\hat{\omega}` at supplied :math:`k`

        Arguments
        ---------
        k: np.ndarray
            array of wavenumber values to calculate :math:`\omega` at
        
        '''
        self.value = np.ones_like(k)
        return self.value
        
        
