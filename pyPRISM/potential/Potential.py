#!python
from __future__ import division,print_function
import numpy as np
class Potential(object):
    '''Baseclass for all intermolecular-pairwise potentials
    
    .. warning:: 
    
     Currently, this class doesn't do anything besides group all of the
     potentials under a single inheritance heirarchy. This will likely
     change as needs arise.
    
    All potentials should inherit from Potential and these subclasses should
    all implement a calculate method. All potential parameters should be specified
    in the constructor except for real-space gridpoints to evaluate the 
    potential at. This information will be provided via  Domain object 
    specified in the System.
    
    '''
        
