#!python
from __future__ import division,print_function
from pyPRISM.omega.Omega import Omega
import numpy as np

class FromArray(Omega):
    '''Read *intra*-molecular correlations from a list or array
    
    This class reads the omega from a Python list or Numpy array.
    
    Attributes
    ----------
    omega: np.ndarray
        Intra-molecular omega

    k: np.narray, *optional*
        Domain of the array data. If provided, this will be checked against the
        Fourier-space grid specified in the :class:`pyPRISM.core.Domain`. An
        exception will be raised is they do not match.

    Example
    -------
    .. code-block:: python

        import pyPRISM
        import numpy as np
        import matplotlib.pyplot as plt

        #set all omega(k) = 1 for type A
        sys = pyPRISM.System(['A','B'],kT=1.0)
        sys.domain = pyPRISM.Domain(dr=0.1,length=1024)
        omega = np.ones(sys.domain.k.shape[0])
        sys.omega['A','A']  = pyPRISM.omega.FromArray(omega)
        x = sys.domain.k
        y = sys.omega['A','A'].calculate(x)

        #plot using matplotlib
        plt.plot(x,y)
        plt.gca().set_xscale("log", nonposx='clip')
        plt.gca().set_yscale("log", nonposy='clip')

        plt.show()

    
    '''
    def __init__(self,omega,k=None):
        r'''Constructor
        
        Arguments
        ---------
        omega: list,np.ndarray
            Python list or Numpy array containing values of omega as
            a function of wavenumber :math:`k`.
            
        k: np.ndarray, *optional*
           Python list of Numpy array containing values of k. These must
           match the k values stored in the :class:`pyPRISM.core.Domain` or an
           exception will be raised. 
        '''
        self.value = np.array(omega)
        self.k = np.array(k)
        
    def __repr__(self):
        return '<Omega: FromArray>'
    
    def calculate(self,k):
        '''Return value of :math:`\hat{\omega}` at supplied :math:`k`

        Arguments
        ---------
        k: np.ndarray
            array of wavenumber values to calculate :math:`\omega` at
        
        '''
        assert self.value.shape[0] == k.shape[0],'Size of array differs from domain!'
        if self.k is not None:
            assert self.k.shape[0] == k.shape[0],'File k-values differ from domain!'
            assert np.allclose(self.k,k),'File k-values differ from domain!'
        return self.value
        
        
