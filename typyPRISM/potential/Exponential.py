#!python
from __future__ import division,print_function
from typyPRISM.potential.Potential import Potential
import numpy as np

class Exponential(Potential):
    r'''Exponential attractive interactions
    
    .. math::
    
        U(r \geq \sigma) - \varepsilon \exp(- \frac{r-\sigma}{\alpha})

    .. math::

        U(r \lt \sigma) = \text{high_value}

    Note
    ----
    :math:`\alpha`
        width of exponential attraction

    :math:`\sigma`
        contact distance of interactions

    :math:`\varepsilon`
        interaction strength

    high_value
        Value to use as overlap potential value. A stand in for :math:`\infty`

    References
    ----------
    Hooper, Schweizer, Macromolecules, 2006, 39 (15), pp 5133
    
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
        
