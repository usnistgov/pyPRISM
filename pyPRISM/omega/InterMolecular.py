#!python
from __future__ import division,print_function
from pyPRISM.omega.NoIntra import NoIntra

class InterMolecular(NoIntra):
    '''alias of NoIntra intra-molecular correlation function '''
    def __repr__(self):
        return '<Omega: InterMolecular>'
    
        
        
