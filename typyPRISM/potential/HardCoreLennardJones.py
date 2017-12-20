#!python
from __future__ import division,print_function
from typyPRISM.potential.Potential import Potential
import numpy as np
class HardCoreLennardJones(Potential):
    r'''12-6 Lennard-Jones potential with Hard Core

    .. warning:: 

        This potential uses a slightly different form than what is 
        implemented for the classic LJ potential in order to match the PRISM
        literature.  This means that the epsilon in the LJ and HCLJ
        potentials will not correspond to the same interaction strengths.
    

    **Mathematical Definition**
    
    .. math::
    
        U_{\alpha,\beta}(r>\sigma_{\alpha,\beta}) = \epsilon_{\alpha,\beta}\big[\big(\frac{\sigma_{\alpha,\beta}}{r}\big)^{12.0} - \big(\frac{\sigma_{\alpha,\beta}}{r}\big)^{6.0}\big]
    
    .. math::
    
        U_{\alpha,\beta}(r\leq\sigma_{\alpha,\beta}) = \infty
    
    
    **Variable Definitions**
    
    :math:`\epsilon_{\alpha,\beta}`
        Strength of interaction (attraction or repulsion) between sites 
	:math:`\alpha` and :math:`\beta`.

    :math:`\sigma_{\alpha,\beta}`
        Length scale of interaction between sites 
	:math:`\alpha` and :math:`\beta`.

    :math:`r`
        Distance between sites. 
    
   
    **Description**

    	Unlike the classic LJ potential, the HCLJ potential has an infinitely
    	hard core and can handle negative and positive epsilons, corresponding
    	to attractive and repulsive interactions.
    
    
    Example
    -------
    .. code-block:: python

        import pyPRISM
	
        #Define a PRISM system and set the A-B interaction potential
	sys = pyPRISM.System(['A','B'],kT=1.0)
	sys.domain = pyPRISM.Domain(dr=0.1,length=1024)
        sys.potential['A','B'] = pyPRISM.potential.HardCoreLennardJones(epsilon=1.0,sigma=1.0,high_value=10**6)

    
    '''
    def __init__(self,epsilon,sigma,high_value=1e6):
        r''' Constructor
        
        Arguments
        ---------
        epsilon: float
            Depth of attractive well
            
        sigma: float
            Contact distance (i.e. low distance where potential magnitude = 0)
            
        high_value: float, *optional*
            value of potential when overlapping
        
        '''
        self.epsilon = epsilon 
        self.sigma = sigma
        self.high_value = high_value
        self.funk  = lambda r: epsilon * ((sigma/r)**(12.0) - 2.0*(sigma/r)**(6.0))
        
    def __repr__(self):
        return '<Potential: HardCoreLennardJones>'
        
    def calculate(self,r):
        r'''Calculate potential values

        Attributes
        ----------
        r: float np.ndarray
            Array of pair distances at which to calculate potential values
        '''
        magnitude = self.funk(r)
        magnitude[r<=self.sigma] = self.high_value
                
        return magnitude
        
