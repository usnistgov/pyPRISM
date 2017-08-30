#!python
from __future__ import division,print_function
from typyPRISM.core.MatrixArray import MatrixArray
from typyPRISM.core.Space import Space
import numpy as np

#XXX Perhaps this should return a table with sentinel None's along the diagonal?
def chi(PRISM):
    '''Calculate the wavenumber-dependent effective interaction parameter (chi)
    
    .. math::
        
        \chi(k)  = 0.5 * \rho * (\hat{C}_{AA}(k) + \hat{C}_{BB}(k) - 2* + \hat{C}_{AB}(k))
        
    Parameters
    ----------
    PRISM: typyPRISM.core.PRISM.PRISM
        A **solved** PRISM object.
    
    Returns
    -------
    chi: dict
        Dictionary of all wavenumber dependent chi pairs indexed by tuple pairs
    
    '''
    
    assert PRISM.rank>1,'the chi calculation is only valid for multicomponent systems'
    
    if PRISM.directCorr.space == Space.Real:
        PRISM.domain.MatrixArray_to_real(PRISM.direcCorr)
        
    totalDensity = 0.
    for i,t1 in enumerate(PRISM.types):
        totalDensity += PRISM.siteDensityMatrix[i,i]
    
    chi = {}
    for i,t1 in enumerate(PRISM.types):
        for j,t2 in enumerate(PRISM.types):
            if i<j:
                C_AA = PRISM.directCorr[i,i]
                C_AB = PRISM.directCorr[i,j]
                C_BB = PRISM.directCorr[j,j]
                
                chi[t1,t2] = chi[t2,t1] = 0.5 * totalDensity * (C_AA + C_BB - 2*C_AB)
                
    
    
    return chi