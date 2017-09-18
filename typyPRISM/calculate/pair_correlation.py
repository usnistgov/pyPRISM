#!python
from __future__ import division,print_function
from typyPRISM.core.Space import Space

def pair_correlation(PRISM):
    r'''Calculate the Real-space pair correlation function 

    Parameters
    ----------
    PRISM: typyPRISM.core.PRISM.PRISM
        A **solved** PRISM object.
    
    Returns
    -------
    pairCorr: typyPRISM.core.MatrixArray.MatrixArray
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
        distribution function* (rdf) or "g of r", the :math:`g(r)` function is
        related to the underlying spatial probability distributions of a given
        system.

        After convergence of a PRISM object, the stored total correlation
        attribute function can simply be shifted to obtain the :math:`g(r)` 


    .. warning::

        Passing an unsolved PRISM object to this function will still produce
        output based on the default values of the attributes of the PRISM
        object.
    

    Example
    -------
    .. code-block:: python

        import typyPRISM

        sys = typyPRISM.System(['A','B'])
        
        sys.domain = typyPRISM.Domain(dr=0.1,length=1024)
        
        sys.density['A'] = 0.1
        sys.density['B'] = 0.75

        sys.diameter[sys.types] = 1.0
        
        sys.closure[sys.types,sys.types] = typyPRISM.closure.PercusYevick()

        sys.potential[sys.types,sys.types] = typyPRISM.potential.HardSphere()
        
        sys.omega['A','A'] = typyPRISM.omega.SingleSite()
        sys.omega['A','B'] = typyPRISM.omega.NoIntra()
        sys.omega['B','B'] = typyPRISM.omega.Gaussian(sigma=1.0,length=10000)
        
        PRISM = sys.createPRISM()

        PRISM.solve()

        rdf = typyPRISM.calculate.pair_correlation(PRISM)

        rdf_AB = rdf['A','B']
    
    '''
    
    if PRISM.totalCorr.space == Space.Fourier:
        PRISM.sys.domain.MatrixArray_to_real(PRISM.totalCorr)
    
    PRISM.pairCorr = PRISM.totalCorr + 1.0
    
    return PRISM.pairCorr
