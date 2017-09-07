#!python
from __future__ import division,print_function
from typyPRISM.core.PairTable import PairTable
from typyPRISM.core.MatrixArray import MatrixArray
from typyPRISM.core.Space import Space
import numpy as np

def chi(PRISM):
    '''Calculate the wavenumber-dependent effective interaction parameter (chi)
    
    .. math::
        
        \chi(k)  = 0.5 * \rho * (\hat{C}_{AA}(k) + \hat{C}_{BB}(k) - 2* + \hat{C}_{AB}(k))
        
    Parameters
    ----------
    PRISM: typyPRISM.core.PRISM
        A **solved** PRISM object.
    
    Returns
    -------
    chi: typyPRISM.core.PairTable
        PairTable of all wavenumber dependent chi pairs indexed by tuple pairs
    
    '''
    
    assert PRISM.sys.rank>1,'The chi calculation is only valid for multicomponent systems'
    
    if PRISM.directCorr.space == Space.Real:
        PRISM.domain.MatrixArray_to_fourier(PRISM.directCorr)
        
    totalDensity = 0.
    for i,t1 in enumerate(PRISM.sys.types):
        totalDensity += PRISM.sys.siteDensityMatrix[i,i]
    
    chi = PairTable(name='chi',types=PRISM.sys.types)
    for i,t1 in enumerate(PRISM.sys.types):
        for j,t2 in enumerate(PRISM.sys.types):
            if i<j:
                C_AA = PRISM.directCorr[t1,t1]
                C_AB = PRISM.directCorr[t1,t2]
                C_BB = PRISM.directCorr[t2,t2]
                
                chi[t1,t2] = 0.5 * totalDensity * (C_AA + C_BB - 2*C_AB)
                
    return chi
