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
        intra-molecular omega

    k: np.narray, *optional*
        domain of the array data. Will be checked against the system
        domain if provided
        
    Example
    -------
    .. code-block:: python

        import pyPRISM
        import numpy as np
        import matplotlib.pyplot as plt

        #Set all omega(k) = 1 for type A
        sys = pyPRISM.System(['A','B'],kT=1.0)
        sys.domain = pyPRISM.Domain(dr=0.1,length=1024)
        omega = np.ones(sys.domain.k.shape[0])
        sys.omega['A','A']  = pyPRISM.omega.FromArray(omega)
        x = sys.domain.k
        y = sys.omega['A','A'].calculate(x)

        #plot it!
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
	    a function of wavenumber, k.
            
        k: np.ndarray, *optional*
           Python list of Numpy array containing values of k. These must
	   match the k values stored in the Domain class.  
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
            array of wavenumber values to caluclate :math:`\omega` at
        
        '''
        assert self.value.shape[0] == k.shape[0],'Size of array differs from supplied domain!'
        if self.k is not None:
            assert self.k.shape[0] == k.shape[0],'Array domain size differs from supplied domain!'
            assert np.allclose(self.k,k),'Array domain differs from supplied domain!'
        return self.value
        
        
