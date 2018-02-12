#!python
from __future__ import division,print_function
from pyPRISM.potential.Potential import Potential
import numpy as np
class HardSphere(Potential):
    r'''Simple hard sphere potential
    

    **Mathematical Definition**
    
    .. math::
    
        U_{\alpha,\beta}(r>\sigma_{\alpha,\beta}) = 0.0
    
    .. math::
    
        U_{\alpha,\beta}(r\leq\sigma_{\alpha,\beta}) = C^{high}
    
    
    **Variable Definitions**
    
    :math:`\sigma_{\alpha,\beta}`
        Length scale of interaction between sites 
	:math:`\alpha` and :math:`\beta`.

    :math:`r`
        Distance between sites. 

    :math:`C^{high}`
        High value used to approximate an infinite potential due to overlap
    
   
    **Description**

        This potential models the simiple hard-sphere fluid, in which sites
        have hard-core repulsion and no interactions outside their contact
        distance.
    
    Example
    -------
    .. code-block:: python

        import pyPRISM
	
        #Define a PRISM system and set the A-B interaction potential
	sys = pyPRISM.System(['A','B'],kT=1.0)
	sys.domain = pyPRISM.Domain(dr=0.1,length=1024)
        sys.potential['A','B'] = pyPRISM.potential.HardSphere(sigma=1.0,high_value=10**6)

    .. warning::

        If sigma is specified such that it does not fall on the solution grid
        of the :class:`~pyPRISM.core.Domain.Domain` object specified in
        :class:`~pyPRISM.core.System.System`, then the sigma will effectively
        be rounded. A warning should be emitted during the construction of a
        :class:`~pyPRISM.core.PRISM.PRISM` object if this occurs.
    
    '''
    def __init__(self,sigma=None,high_value=1e6):
        r''' Constructor
        
        Arguments
        ---------
        sigma: float, *optional*
            Contact distance. If not specified, sigma will be calculated from 
            the diameters specified in the :class:`~pyPRISM.core.System.System`
            object.
            
        high_value: float, *optional*
            High value used to approximate an infinite potential due to overlap
        '''
        self.sigma = sigma
        self.high_value = high_value
        self.funk  = lambda r,sigma: np.where(r>sigma,0.0,high_value)
    def __repr__(self):
        return '<Potential: HardSphere>'
    
    def calculate(self,r):
        r'''Calculate value of potential

        Attributes
        ----------
        r: float np.ndarray
            Array of pair distances at which to calculate potential values
        '''
        assert (self.sigma is not None), 'Sigma must be set before evaluating potential!'

        magnitude = self.funk(r,self.sigma)
        return magnitude
        
