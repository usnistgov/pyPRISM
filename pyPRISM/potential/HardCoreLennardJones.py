#!python
from __future__ import division,print_function
from pyPRISM.potential.Potential import Potential
import numpy as np
class HardCoreLennardJones(Potential):
    r'''12-6 Lennard-Jones potential with Hard Core

    .. warning:: 

        This potential uses a slightly different form than what is 
        implemented for the classic LJ potential. This means that the epsilon
        in the LJ and HCLJ potentials will not correspond to the same
        interaction strengths.

    **Mathematical Definition**
    
    .. math::
    
        U_{\alpha,\beta}(r>\sigma_{\alpha,\beta}) = \epsilon_{\alpha,\beta}\left[\left(\frac{\sigma_{\alpha,\beta}}{r}\right)^{12} - 2 \left(\frac{\sigma_{\alpha,\beta}}{r}\right)^{6}\right]
    
    .. math::
    
        U_{\alpha,\beta}(r\leq\sigma_{\alpha,\beta}) = C^{high}
    
    
    **Variable Definitions**
    
    :math:`\epsilon_{\alpha,\beta}`
        Strength of interaction (attraction or repulsion) between sites 
	:math:`\alpha` and :math:`\beta`.

    :math:`\sigma_{\alpha,\beta}`
        Length scale of interaction between sites 
	:math:`\alpha` and :math:`\beta`.

    :math:`r`
        Distance between sites. 

    :math:`C^{high}`
        High value used to approximate an infinite potential due to overlap
    
   
    **Description**

    	Unlike the classic LJ potential, the HCLJ potential has an infinitely
    	hard core and can handle negative and positive epsilons, corresponding
    	to attractive and repulsive interactions.

    References
    ----------
    #. Yethiraj, A. and K.S. Schweizer, INTEGRAL-EQUATION THEORY OF POLYMER
       BLENDS - NUMERICAL INVESTIGATION OF MOLECULAR CLOSURE APPROXIMATIONS.
       Journal of Chemical Physics, 1993. 98(11): p. 9080-9093.
       [`link <https://doi.org/10.1063/1.464466>`__]
    
    
    Example
    -------
    .. code-block:: python

        import pyPRISM
	
        #Define a PRISM system and set the A-B interaction potential
	sys = pyPRISM.System(['A','B'],kT=1.0)
	sys.domain = pyPRISM.Domain(dr=0.1,length=1024)
        sys.potential['A','B'] = pyPRISM.potential.HardCoreLennardJones(epsilon=1.0,sigma=1.0,high_value=10**6)

    .. warning::

        If sigma is specified such that it does not fall on the solution grid
        of the :class:`~pyPRISM.core.Domain.Domain` object specified in
        :class:`~pyPRISM.core.System.System`, then the sigma will effectively
        be rounded. A warning should be emitted during the construction of a
        :class:`~pyPRISM.core.PRISM.PRISM` object if this occurs.
    
    '''
    def __init__(self,epsilon,sigma=None,high_value=1e6):
        r''' Constructor
        
        Arguments
        ---------
        epsilon: float
            Depth of attractive well
            
        sigma: float, *optional*
            Contact distance. If not specified, sigma will be calculated from 
            the diameters specified in the :class:`~pyPRISM.core.System.System`
            object.
            
        high_value: float, *optional*
            High value used to approximate an infinite potential due to overlap
        
        '''
        self.epsilon = epsilon 
        self.sigma = sigma
        self.high_value = high_value
        self.funk  = lambda r,sigma: epsilon * ((sigma/r)**(12.0) - 2.0*(sigma/r)**(6.0))
        
    def __repr__(self):
        return '<Potential: HardCoreLennardJones>'
        
    def calculate(self,r):
        r'''Calculate value of potential

        Attributes
        ----------
        r: float np.ndarray
            Array of pair distances at which to calculate potential values
        '''
        assert (self.sigma is not None), 'Sigma must be set before evaluating potential!'

        magnitude = self.funk(r,self.sigma)
        magnitude[r<=self.sigma] = self.high_value
                
        return magnitude
        
