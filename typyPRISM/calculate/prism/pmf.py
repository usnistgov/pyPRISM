#!python
from __future__ import division,print_function
from typyPRISM.core.MatrixArray import MatrixArray
from typyPRISM.core.Space import Space
from typyPRISM.calculate.prism.pair_correlation import pair_correlation
import numpy as np

def pmf(PRISM):
    '''Calculate the potentials of mean force from a PRISM object
    
    .. math::
        W(r) = -k_{B} T log(h(r)+1.0)
        
    Parameters
    ----------
    PRISM: typyPRISM.core.PRISM.PRISM
        A **solved** PRISM object.
    
    Returns
    -------
    pmf: typyPRISM.core.MatrixArray.MatrixArray
        The full MatrixArray of potentials of mean force
    
    '''
    rdf = pair_correlation(PRISM)
    
    #let's ignore any warnings about negative values in the log function
    with np.errstate(invalid='ignore'):
        rdf = -1.0 * PRISM.kT * np.log(rdf.data)
    
    #length and rank will be inferred from data
    pmf = MatrixArray(data=rdf,space=Space.Real,length=None,rank=None)
    
    return pmf