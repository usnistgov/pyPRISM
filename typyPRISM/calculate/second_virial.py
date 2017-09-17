#!python
from __future__ import division,print_function
from typyPRISM.core.Space import Space
from typyPRISM.core.PairTable import PairTable

def second_virial(PRISM):
    '''Calculate the second virial coefficient from a PRISM object

    .. warning:: 

        This function does not interpolate to the k=0, and instead
        just reports the lowest k value in the PRISM domain. This may
        be changed in the future. 
    
    .. math::

        B2 = -0.5*h(k->0)
        
    Parameters
    ----------
    PRISM: typyPRISM.core.PRISM.PRISM
        A **solved** PRISM object.
    
    Returns
    -------
    B2: typyPRISM.core.PairTable
        Pairtable of B2 values
    
    '''
    
    if PRISM.totalCorr.space == Space.Real:
        PRISM.sys.domain.MatrixArray_to_fourier(PRISM.totalCorr)
    
    B2 = PairTable(name='B2',types=PRISM.sys.types)
    for i,t1 in enumerate(PRISM.sys.types):
        for j,t2 in enumerate(PRISM.sys.types):
            B2[t1,t2] = - 0.5 * PRISM.totalCorr[t1,t2][0]
    
    return B2
