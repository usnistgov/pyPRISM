from typyPRISM.intraMolCorr.IntraMolCorr import IntraMolCorr
import numpy as np

class NoIntra(IntraMolCorr):
    '''inter-molecule intra-molecular correlation function
    
    This is a convenience class for specifying the intra-molecular
    correlations between sites which are never in the same molecule.
    Because they have no *intra*-molecular correlation, this function
    returns zero at all wavenumber.
    
    '''
    def __repr__(self):
        return '<IntraMolCorr: NoIntra>'
    
    def calculate(self,k):
        self.value = np.zeros_like(k)
        return self.value
        
        