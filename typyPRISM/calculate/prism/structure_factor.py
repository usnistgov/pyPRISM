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
        PRISM.domain.MatrixArray_to_real(PRISM.totalCorr)
        
    if PRISM.intraMolCorr.space == Space.Real:
        PRISM.domain.MatrixArray_to_real(PRISM.intraMolCorr)
    
    structureFactor = PRISM.totalCorr*PRISM.pairDensityMatrix + PRISM.intraMolCorr
    
    return structureFactor