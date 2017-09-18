#!python
from __future__ import division,print_function
from typyPRISM.core.Space import Space

def pair_correlation(PRISM):
    r'''Calculate the pair correlation function from a PRISM object
    
    After convergence, the stored total correlation function can 
    simply be shifted to obtain the pair-correlation function 
    i.e. the radial distribution function. 
    
    .. math::

        g_{\alpha,\beta}(r) = h_{\alpha,\beta}(r) + 1.0
        
    Parameters
    ----------
    PRISM: typyPRISM.core.PRISM.PRISM
        A **solved** PRISM object.
    
    Returns
    -------
    pairCorr: typyPRISM.core.MatrixArray.MatrixArray
        The full MatrixArray of pair correlation functions.

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
        sys.potential[sys.types,sys.types] = typyPRISM.closure.HardSphere()
        
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
