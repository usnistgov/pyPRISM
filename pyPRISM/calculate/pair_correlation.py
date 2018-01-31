#!python
from __future__ import division,print_function
from pyPRISM.core.Space import Space

def pair_correlation(PRISM):
    r'''Calculate the Real-space *inter*-molecular pair correlation function 

    Parameters
    ----------
    PRISM: pyPRISM.core.PRISM
        A **solved** PRISM object.
    
    Returns
    -------
    pairCorr: pyPRISM.core.MatrixArray
        The full MatrixArray of pair correlation functions.
    

    **Mathematical Definition**

    .. math::
         
        g_{\alpha,\beta}(r) = h_{\alpha,\beta}(r) + 1.0
    
    **Variable Definitions**

        - :math:`g_{\alpha,\beta}(r)`
            Pair correlation function between site types :math:`\alpha` and
            :math:`\beta` at a distance :math:`r`

        - :math:`h_{\alpha,\beta}(r)`
            Total correlation function between site types :math:`\alpha` and
            :math:`\beta` at a distance :math:`r`

    **Description**

        The pair correlation function describes the spatial correlations
        between pairs of sites in Real-space. Also known as the *radial
        distribution function* (rdf), the :math:`g(r)` function is
        related to the underlying spatial probability distributions of a given
        system. In a PRISM calculation, :math:`g(r)` is strictly an
        *inter*-molecular quantity.

        After convergence of a PRISM object, the stored total correlation
        attribute function can simply be shifted to obtain the :math:`g(r)` 


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

        rdf = pyPRISM.calculate.pair_correlation(PRISM)

        rdf_AA = rdf['A','A']
        rdf_AB = rdf['A','B']
        rdf_BB = rdf['B','B']
    
    '''
    
    if PRISM.totalCorr.space == Space.Fourier:
        PRISM.sys.domain.MatrixArray_to_real(PRISM.totalCorr)
    
    PRISM.pairCorr = PRISM.totalCorr + 1.0
    
    return PRISM.pairCorr
