#!python
from __future__ import division,print_function
from typyPRISM.core.Space import Space

def structure_factor(PRISM):
    '''Calculate the structure factor from a PRISM object
    
    .. math::
        S(k) = \omega(k) + h(k)
        
    Parameters
    ----------
    PRISM: typyPRISM.core.PRISM.PRISM
        A **solved** PRISM object.
    
    Returns
    -------
    structureFactor: typyPRISM.core.MatrixArray.MatrixArray
        The full MatrixArray of structure factors
    
    '''
    
    if PRISM.totalCorr.space == Space.Real:
        PRISM.sys.domain.MatrixArray_to_fourier(PRISM.totalCorr)
        
    if PRISM.omega.space == Space.Real:
        PRISM.sys.domain.MatrixArray_to_fourier(PRISM.omega)
    
    structureFactor = (PRISM.totalCorr*PRISM.sys.pairDensityMatrix + PRISM.omega)/PRISM.sys.siteDensityMatrix
    # structureFactor = PRISM.totalCorr + PRISM.omega
    
    return structureFactor
