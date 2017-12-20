#!python
from __future__ import division,print_function
from pyPRISM.core.MatrixArray import MatrixArray
from pyPRISM.core.Space import Space
from pyPRISM.calculate.pair_correlation import pair_correlation
import numpy as np

def pmf(PRISM):
    r'''Calculate the potentials of mean force

    Parameters
    ----------
    PRISM: pyPRISM.core.PRISM
        A **solved** PRISM object.
    
    Returns
    -------
    pmf: pyPRISM.core.MatrixArray
        The full MatrixArray of potentials of mean force

    
    **Mathematical Definition**

    .. math::

        w_{\alpha,\beta}(r) = -k_{B} T \ln(h_{\alpha,\beta}(r)+1.0)
    
    **Variable Definitions**

        - :math:`w_{\alpha,\beta}(r)`
            Potential of mean force between site types :math:`\alpha` and
            :math:`\beta` at a distance :math:`r`

        - :math:`g_{\alpha,\beta}(r)`
            Pair correlation function between site types :math:`\alpha` and
            :math:`\beta` at a distance :math:`r`

        - :math:`h_{\alpha,\beta}(r)`
            Total correlation function between site types :math:`\alpha` and
            :math:`\beta` at a distance :math:`r`

    **Description**

        A potential of mean force (PMF) between site types :math:`\alpha` and
        :math:`\beta`, :math:`w_{\alpha,\beta}` represents the the ensemble
        averaged free energy change needed to bring these two sites from
        infinite separation to a distance :math:`r`. It can also be thought of
        as a potential that would be needed to reproduce the underlying
        :math:`g_{\alpha,\beta}(r)`. 


    .. warning::

        Passing an unsolved PRISM object to this function will still produce
        output based on the default values of the attributes of the PRISM
        object.
    

    Example
    -------
    .. code-block:: python

        import pyPRISM

        sys = pyPRISM.System(['A','B'])

        # ** populate system variables **
        
        PRISM = sys.createPRISM()

        PRISM.solve()

        pmf = pyPRISM.calculate.pmf(PRISM)

        pmf_BB = pmf['B','B']
    
    
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
