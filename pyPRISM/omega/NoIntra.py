#!python
from __future__ import division,print_function
from pyPRISM.omega.Omega import Omega
import numpy as np

class NoIntra(Omega):
    '''Inter-molecule intra-molecular correlation function
    
    **Description**
        This is a convenience class for specifying the intra-molecular
        correlations between sites which are never in the same molecule.
        Because they have no *intra*-molecular correlation, this function
        returns zero at all wavenumber.
    
    Example
    -------
    .. code-block:: python

        import pyPRISM
        import numpy as np
        import matplotlib.pyplot as plt

        #set omega(k) for types A,B to have no intra-molecular
        #correlations (sites A and B are never on the same molecule)
        sys = pyPRISM.System(['A','B'],kT=1.0)
        sys.domain = pyPRISM.Domain(dr=0.1,length=1024)
        sys.omega['A','B']  = pyPRISM.omega.NoIntra()
        x = sys.domain.k
        y = sys.omega['A','B'].calculate(x)

        #plot using matplotlib
        plt.plot(x,y)
        plt.gca().set_xscale("log", nonposx='clip')
        plt.gca().set_yscale("log", nonposy='clip')

        plt.show()
    
    '''
    def __repr__(self):
        return '<Omega: NoIntra>'
    
    def calculate(self,k):
        '''Return value of :math:`\hat{\omega}` at supplied :math:`k`

        Arguments
        ---------
        k: np.ndarray
            array of wavenumber values to calculate :math:`\omega` at
        
        '''
        self.value = np.zeros_like(k)
        return self.value

        
