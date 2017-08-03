from typyPRISM.core.Space import Space

def pair_correlation(PRISM):
    '''Calculate the pair correlation function from a PRISM object
    
    After convergence, the stored total correlation function can 
    simply be shifted to obtain the pair-correlation function 
    i.e. the radial distribution function. 
    
    .. math::
        g(r) = h(r) + 1.0
        
    Parameters
    ----------
    PRISM: typyPRISM.core.PRISM.PRISM
        A **solved** PRISM object.
    
    
    Returns
    -------
    pairCorr: typyPRISM.core.MatrixArray.MatrixArray
        The full MatrixArray of pair correlation functions.
    
    '''
    
    if PRISM.totalCorr.space == Space.Fourier:
        PRISM.domain.MatrixArray_to_real(PRISM.totalCorr)
    
    PRISM.pairCorr = PRISM.totalCorr + 1.0
    
    return PRISM.pairCorr