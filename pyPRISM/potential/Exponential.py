#!python
from __future__ import division,print_function
from pyPRISM.potential.Potential import Potential
import numpy as np

class Exponential(Potential):
    r'''Exponential attractive interactions
    
    
    **Mathematical Definition**
    
    .. math::
    
        U_{\alpha,\beta}(r \geq \sigma_{\alpha,\beta}) - \epsilon_{\alpha,\beta} \exp(- \frac{r-\sigma_{\alpha,\beta}}{\alpha})

    .. math::

        U_{\alpha,\beta}(r \lt \sigma_{\alpha,\beta}) = \infty

    
    **Variable Definitions**
    
    :math:`\alpha`
        Width of exponential attraction

    :math:`\sigma_{\alpha,\beta}`
        Contact distance of interactions between sites 
	:math:`\alpha` and :math:`\beta`.


    :math:`\epsilon_{\alpha,\beta}`
        Interaction strength between sites 
	:math:`\alpha` and :math:`\beta`.
    

    **Description**

    	This potential models an exponential-like attraction between sites with
	a specified site size and contact distance. For example, in the below
	reference, this potential is used to model the attraction between a 
	nanoparticle and monomers of a polymer chain. 


    References
    ----------
    Hooper, Schweizer, Macromolecules, 2006, 39 (15), pp 5133
    

    Example
    -------
    .. code-block:: python

        import pyPRISM
	
        #Define a PRISM system and set the A-B interaction potential
	sys = pyPRISM.System(['A','B'],kT=1.0)
	sys.domain = pyPRISM.Domain(dr=0.1,length=1024)
        sys.potential['A','B'] = pyPRISM.potential.Exponential(epsilon=1.0,sigma=8.0,alpha=0.5,high_value=10**6)

    
    '''
    def __init__(self,epsilon,sigma,alpha,high_value=1e6):
        r''' Constructor
        
        Arguments
        ---------
        epsilon: float
            strength of attraction
            
        sigma: float
            contact distance 
            
        alpha: float
            range of attraction
            
        high_value: float, *optional*
            value of potential when overlapping
        
        '''
        self.epsilon = epsilon
        self.sigma = sigma
        self.alpha = alpha
        self.high_value = high_value
        self.funk  = lambda r: - epsilon * np.exp(-(r-sigma)/(alpha))
    def __repr__(self):
        return '<Potential: Exponential>'
    
    def calculate(self,r):
        r'''Calculate potential values

        Attributes
        ----------
        r: float np.ndarray
            Array of pair distances at which to calculate potential values
        '''
        magnitude = self.funk(r)
        magnitude = np.where(r>self.sigma,magnitude,self.high_value)
        return magnitude
        
