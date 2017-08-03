from typyPRISM.intraMolCorr.IntraMolCorr import IntraMolCorr
import numpy as np

class SingleSite(IntraMolCorr):
    '''Single-site intra-molecular correlation function
    
    This class is useful for dealing with single bead molecules
    such as solvent or large particles. 
    
    '''
    def __repr__(self):
        return '<IntraMolCorr: SingleSite>'
    
    def calculate(self,k):
        self.value = np.ones_like(k)
        return self.value
        
        