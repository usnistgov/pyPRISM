#!python
from __future__ import division,print_function
from pyPRISM.omega.Omega import Omega
import numpy as np

class FromFile(Omega):
    '''Read *intra*-molecular correlations from file
    
    This class reads a one or two column file using Numpy's
    loadtxt function. A one-column file is expected to only
    contain intra-molecular correlation data, while a two-column
    file contains the k values of the data in the first column
    as well. If the k-values are provided, an extra check to make
    sure that the file data matches the same k-space grid of the
    domain. 
    
    Attributes
    ----------
    fileName: str
        full path + name to column file
        
    Example
    -------
    .. code-block:: python

        import pyPRISM
        import numpy as np
        import matplotlib.pyplot as plt

        #set type A omega(k) from a file
        sys = pyPRISM.System(['A','B'],kT=1.0)
        sys.domain = pyPRISM.Domain(dr=0.1,length=1024)
        fileName = './test_example_filename.txt'
        sys.omega['A','A']  = pyPRISM.omega.FromFile(fileName)
        x = sys.domain.k
        y = sys.omega['A','A'].calculate(x)

        #plot using matplotlib
        plt.plot(x,y)
        plt.gca().set_xscale("log", nonposx='clip')
        plt.gca().set_yscale("log", nonposy='clip')

        plt.show()

    
    '''
    def __init__(self,fileName):
        r'''Constructor
        
        Arguments
        ---------
        fileName: str
            path to textfile containing values of omega as
	    a function of wavenumber, k.
            
        '''
        self.fileName = fileName
        
    def __repr__(self):
        return '<Omega: FromFile>'
    
    def calculate(self,k):
        '''Return value of :math:`\hat{\omega}` at supplied :math:`k`

        Arguments
        ---------
        k: np.ndarray
            array of wavenumber values to calculate :math:`\omega` at
        
        '''
        fileData = np.loadtxt(self.fileName)
        
        if len(fileData.shape)>=2:
            assert fileData.shape[0] == k.shape[0],'Domain size of file differs from supplied domain!'
            assert np.allclose(fileData[:,0],k),'Domain of file differs from supplied domain!'
            self.value = fileData[:,1]
        else:
            self.value = fileData
        
        return self.value
        
        
