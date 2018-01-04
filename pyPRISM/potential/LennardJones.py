#!python
from __future__ import division,print_function
from pyPRISM.potential.Potential import Potential
import numpy as np
class LennardJones(Potential):
    r'''12-6 Lennard-Jones potential
    

    **Mathematical Definition**
    
    .. math::
    
        U_{\alpha,\beta}(r) = 4\epsilon_{\alpha,\beta}\big[\big(\frac{\sigma_{\alpha,\beta}}{r}\big)^{12.0} - \big(\frac{\sigma_{\alpha,\beta}}{r}\big)^{6.0}\big]
    
    
    **Variable Definitions**
    
    :math:`\epsilon_{\alpha,\beta}`
        Strength of attraction between sites :math:`\alpha` and :math:`\beta`.

    :math:`\sigma_{\alpha,\beta}`
        Length scale of interaction between sites :math:`\alpha` and
        :math:`\beta`.

    :math:`r`
        Distance between sites. 
    
   
    **Description**

    	The classic 12-6 LJ potential. To facilitate direct comparison with
    	molecular simulation, the simulation may be cut and shifted to zero 
    	at a specified cutoff distance by setting the rcut and shift parameters.
    	The full (non-truncated) LJ potential is accessed using rcut=None and 
    	shift=False. 
    
    
    Example
    -------
    .. code-block:: python

        import pyPRISM

        #Define a PRISM system and set the A-B interaction potential
        sys = pyPRISM.System(['A','B'],kT=1.0)
        sys.domain = pyPRISM.Domain(dr=0.1,length=1024)
        sys.potential['A','B'] = pyPRISM.potential.LennardJones(epsilon=1.0,sigma=1.0,rcut=2.5,shift=True)

    
    '''
    def __init__(self,epsilon,sigma,rcut=None,shift=False):
        r''' Constructor
        
        Arguments
        ---------
        epsilon: float
            Depth of attractive well
            
        sigma: float
            Contact distance (i.e. low distance where potential magnitude = 0)
            
        rcut: float, *optional*
            Cutoff distance for potential. Useful for comparing directly to results
            from simulations where cutoffs are necessary. 
    
        shift: bool,*optional*
            Shift the potential by its value at the cutoff. Clearly this only makes 
            sense if rcut is specified
    
        '''
        self.epsilon = epsilon
        self.sigma = sigma
        self.rcut  = rcut
        self.shift = shift
        self.funk  = lambda r: 4 * epsilon * ((sigma/r)**(12.0) - (sigma/r)**(6.0))
        
    def __repr__(self):
        return '<Potential: LennardJones>'
        
    def calculate(self,r):
        r'''Calculate potential values

        Attributes
        ----------
        r: float np.ndarray
            Array of pair distances at which to calculate potential values
        '''
        magnitude = self.funk(r)
        
        if self.rcut is not None:
            if self.shift:
                magnitude -= self.funk(self.rcut)
            magnitude[r>self.rcut] = 0.0
                
        return magnitude

    def calculate_attractive(self,r):
        r'''Calculate the attractive tail of the Lennard Jones potential
        '''
        magnitude = np.zeros_like(r)
        mask = r>self.sigma
        magnitude[mask] = self.calculate(r)[mask]
        return magnitude
        
