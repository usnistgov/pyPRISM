#!python
from __future__ import division,print_function
from pyPRISM.potential.Potential import Potential
import numpy as np

class Exponential(Potential):
    r'''Exponential attractive interactions
    
    
    **Mathematical Definition**
    
    .. math::
    
        U_{\alpha,\beta}(r \geq \sigma_{\alpha,\beta}) = \epsilon_{\alpha,\beta} \exp\left(- \frac{r-\sigma_{\alpha,\beta}}{\alpha}\right)

    .. math::

        U_{\alpha,\beta}(r < \sigma_{\alpha,\beta}) = C^{high}

    
    **Variable Definitions**
    
    :math:`\alpha`
        Width of exponential attraction

    :math:`\sigma_{\alpha,\beta}`
        Contact distance of interactions between sites 
	:math:`\alpha` and :math:`\beta`.


    :math:`\epsilon_{\alpha,\beta}`
        Interaction strength between sites 
	:math:`\alpha` and :math:`\beta`.

    :math:`C^{high}`
        High value used to approximate an infinite potential due to overlap
    

    **Description**

    	This potential models an exponential-like attraction between sites with
        a specified site size and contact distance. For example, in Reference
        [1] this potential is used to model the attraction between a 
	nanoparticle and monomers of a polymer chain. 


    References
    ----------
    #. Hooper, J.B. and K.S. Schweizer, Theory of phase separation in polymer
       nanocomposites. Macromolecules, 2006. 39(15): p. 5133-5142.
       [`link <https://doi.org/10.1021/ma060577m>`__]

    

    Example
    -------
    .. code-block:: python

        import pyPRISM
	
        #Define a PRISM system and set the A-B interaction potential
	sys = pyPRISM.System(['A','B'],kT=1.0)
	sys.domain = pyPRISM.Domain(dr=0.1,length=1024)
        sys.potential['A','B'] = pyPRISM.potential.Exponential(epsilon=1.0,sigma=8.0,alpha=0.5,high_value=10**6)

    .. warning::

        If sigma is specified such that it does not fall on the solution grid
        of the :class:`~pyPRISM.core.Domain.Domain` object specified in
        :class:`~pyPRISM.core.System.System`, then the sigma will effectively
        be rounded. A warning should be emitted during the construction of a
        :class:`~pyPRISM.core.PRISM.PRISM` object if this occurs.
    
    '''
    def __init__(self,epsilon,alpha,sigma=None,high_value=1e6):
        r''' Constructor
        
        Arguments
        ---------
        epsilon: float
            Strength of attraction
            
        alpha: float
            Range of attraction

        sigma: float, *optional*
            Contact distance. If not specified, sigma will be calculated from 
            the diameters specified in the :class:`~pyPRISM.core.System.System`
            object.
            
        high_value: float, *optional*
            High value used to approximate an infinite potential due to overlap
        
        '''
        self.epsilon = epsilon
        self.sigma = sigma
        self.alpha = alpha
        self.high_value = high_value
        self.funk  = lambda r,sigma: - epsilon * np.exp(-(r-sigma)/(alpha))
    def __repr__(self):
        return '<Potential: Exponential>'
    
    def calculate(self,r):
        r'''Calculate the value of the potential

        Attributes
        ----------
        r: float np.ndarray
            Array of pair distances at which to calculate potential values
        '''
        assert (self.sigma is not None), 'Sigma must be set before evaluating potential!'

        magnitude = self.funk(r,self.sigma)
        magnitude = np.where(r>self.sigma,magnitude,self.high_value)
        return magnitude
        
