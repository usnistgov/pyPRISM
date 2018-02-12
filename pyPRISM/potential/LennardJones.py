#!python
from __future__ import division,print_function
from pyPRISM.potential.Potential import Potential
import numpy as np

class LennardJones(Potential):
    r'''12-6 Lennard-Jones potential
    

    **Mathematical Definition**
    
    .. math::
    
        U_{\alpha,\beta}(r) = 4\epsilon_{\alpha,\beta}\left[\left(\frac{\sigma_{\alpha,\beta}}{r}\right)^{12.0} - \left(\frac{\sigma_{\alpha,\beta}}{r}\right)^{6.0}\right]

    .. math::
    
        U_{\alpha,\beta}^{shift}(r) = U_{\alpha,\beta}(r) - U_{\alpha,\beta}(r_{cut})
    
    
    **Variable Definitions**
    
    :math:`\epsilon_{\alpha,\beta}`
        Strength of attraction between sites :math:`\alpha` and :math:`\beta`.

    :math:`\sigma_{\alpha,\beta}`
        Length scale of interaction between sites :math:`\alpha` and
        :math:`\beta`.

    :math:`r`
        Distance between sites. 
    
    :math:`r_{cut}`
        Cutoff distance between sites. 
   
    **Description**

        The classic 12-6 LJ potential. To facilitate direct comparison with
        molecular simulation, the simulation may be cut and shifted to zero at
        a specified cutoff distance by setting the rcut and shift parameters.
        The full (non-truncated) LJ potential is accessed using
        :math:`r_{cut}` =  *None* and :math:`shift` = *False*.
    
    
    Example
    -------
    .. code-block:: python

        import pyPRISM

        #Define a PRISM system and set the A-B interaction potential
        sys = pyPRISM.System(['A','B'],kT=1.0)
        sys.domain = pyPRISM.Domain(dr=0.1,length=1024)
        sys.potential['A','B'] = pyPRISM.potential.LennardJones(epsilon=1.0,sigma=1.0,rcut=2.5,shift=True)

    .. warning::

        If sigma is specified such that it does not fall on the solution grid
        of the :class:`~pyPRISM.core.Domain.Domain` object specified in
        :class:`~pyPRISM.core.System.System`, then the sigma will effectively
        be rounded. A warning should be emitted during the construction of a
        :class:`~pyPRISM.core.PRISM.PRISM` object if this occurs.

    
    '''
    def __init__(self,epsilon,sigma=None,rcut=None,shift=False):
        r''' Constructor
        
        Arguments
        ---------
        epsilon: float
            Depth of attractive well
            
        sigma: float, *optional*
            Contact distance. If not specified, sigma will be calculated from 
            the diameters specified in the :class:`~pyPRISM.core.System.System`
            object.
            
        rcut: float, *optional*
            Cutoff distance for potential. Useful for comparing directly to results
            from simulations where cutoffs are necessary. 
    
        shift: bool,*optional*
            If :math:`r_{cut}` is specified, shift the potential by its value
            at the cutoff. If :math:`r_{cut}` is not specified, this parameter
            is ignored.
    
        '''
        self.epsilon = epsilon
        self.sigma = sigma
        self.rcut  = rcut
        self.shift = shift
        self.funk  = lambda r,s: 4 * epsilon * ((s/r)**(12.0) - (s/r)**(6.0))
        
    def __repr__(self):
        return '<Potential: LennardJones>'
        
    def calculate(self,r):
        r'''Calculate value of potential

        Attributes
        ----------
        r: float np.ndarray
            Array of pair distances at which to calculate potential values
        '''
        assert (self.sigma is not None), 'Sigma must be set before evaluating potential!'

        magnitude = self.funk(r,self.sigma)
        
        if self.rcut is not None:
            if self.shift:
                magnitude -= self.funk(self.rcut,self.sigma)
            magnitude[r>self.rcut] = 0.0
                
        return magnitude

    def calculate_attractive(self,r):
        r'''Calculate the attractive tail of the Lennard Jones potential. Returns zero at :math:`r<\sigma`
        '''
        assert (self.sigma is not None), 'Sigma must be set before evaluating potential!'

        magnitude = np.zeros_like(r)
        mask = r>self.sigma
        magnitude[mask] = self.calculate(r,self.sigma)[mask]
        return magnitude
        
