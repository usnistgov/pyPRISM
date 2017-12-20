#!python
from __future__ import division,print_function
from typyPRISM.potential.Potential import Potential
import numpy as np
class HardSphere(Potential):
    r'''Simple hard sphere potential
    

    **Mathematical Definition**
    
    .. math::
    
        U_{\alpha,\beta}(r>\sigma_{\alpha,\beta}) = 0.0
    
    .. math::
    
        U_{\alpha,\beta}(r\leq\sigma_{\alpha,\beta}) = \infty
    
    
    **Variable Definitions**
    
    :math:`\sigma_{\alpha,\beta}`
        Length scale of interaction between sites 
	:math:`\alpha` and :math:`\beta`.

    :math:`r`
        Distance between sites. 
    
   
    **Description**

    	This potential models the simiple hard-sphere fluid, in which 
    	sites have no interactions outside their contact distance, and
    	hard-core repulsion.
    
    
    Example
    -------
    .. code-block:: python

        import pyPRISM
	
        #Define a PRISM system and set the A-B interaction potential
	sys = pyPRISM.System(['A','B'],kT=1.0)
	sys.domain = pyPRISM.Domain(dr=0.1,length=1024)
        sys.potential['A','B'] = pyPRISM.potential.HardSphere(sigma=1.0,high_value=10**6)

    
    '''
    def __init__(self,sigma,high_value=1e6):
        r''' Constructor
        
        Arguments
        ---------
        sigma: float
            Contact distance 
            
        high_value: float, *optional*
            value of potential when overlapping
        
        '''
        self.sigma = sigma
        self.high_value = high_value
        self.funk  = lambda r: np.where(r>sigma,0.0,high_value)
    def __repr__(self):
        return '<Potential: HardSphere>'
    
    def calculate(self,r):
        r'''Calculate potential values

        Attributes
        ----------
        r: float np.ndarray
            Array of pair distances at which to calculate potential values
        '''
        magnitude = self.funk(r)
        return magnitude
        
