#!python
from __future__ import division,print_function
from typyPRISM.core.MatrixArray import MatrixArray
from typyPRISM.core.Space import Space
from typyPRISM.calculate.pair_correlation import pair_correlation
import numpy as np

def pmf(PRISM):
    r'''Calculate the potentials of mean force from a PRISM object

    A potential of mean force (PMF) between site types :math:`\alpha` and
    :math:`\beta`, :math:`w_{\alpha,\beta}` represents the the ensemble averaged
    free energy change needed to bring these two sites from infinite separation
    to a distance :math:`r`. It can also be thought of as a potential that would
    be needed to reproduce the underlying :math:`g_{\alpha,\beta}(r)`. 
    
    .. math::

        w_{\alpha,\beta}(r) = -k_{B} T \log(h_{\alpha,\beta}(r)+1.0)
        
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
        rdf = -1.0 * PRISM.sys.kT * np.log(rdf.data)
    
    #length and rank will be inferred from data
    pmf = MatrixArray(data=rdf,
                      space=Space.Real,
                      length=None,
                      rank=None,
                      types=PRISM.sys.types)
    
    return pmf
