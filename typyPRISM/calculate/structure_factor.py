#!python
from __future__ import division,print_function
from typyPRISM.core.Space import Space

def structure_factor(PRISM,normalize=True):
    r'''Calculate the structure factor from a PRISM object
    
        
    Parameters
    ----------
    PRISM: typyPRISM.core.PRISM
        A **solved** PRISM object.

    normalize: bool
        normalize the structure factor by the site density
    
    Returns
    -------
    structureFactor: typyPRISM.core.MatrixArray
        The full MatrixArray of structure factors

        
    **Mathematical Definition**


    .. math::

        \hat{s}_{\alpha,\beta}(k) = \rho^{site}_{\alpha,\beta} \hat{\omega}_{\alpha,\beta}(k) + \rho^{pair}_{\alpha,\beta} \hat{h}_{\alpha,\beta}(k)

    
    **Variable Definitions**

        - :math:`\hat{\omega}_{\alpha,\beta}(k)`
            Intra-molecular correlation function between sites :math:`\alpha`
            and :math:`\beta` at a wavenumber :math:`k`

        - :math:`\hat{h}_{\alpha,\beta}(k)`
            Total correlation function between sites :math:`\alpha` and
            :math:`\beta` at a wavenumber :math:`k`

        - :math:`\rho^{site}_{\alpha,\beta}`, :math:`\rho^{pair}_{\alpha,\beta}`
            Sitewise and pairwise densities for sites :math:`\alpha` and
            :math:`\beta`. See :class:`typyPRISM.core.Density` for details. 

    **Description**

        To be added...


    .. warning::

        Passing an unsolved PRISM object to this function will still produce
        output based on the default values of the attributes of the PRISM
        object.
    
    
    References
    ----------
    Schweizer, Curro, Thermodynamics of Polymer Blends,
    J. Chem. Phys., 1989 91 (8) 5059


    Example
    -------
    .. code-block:: python

        import typyPRISM

        sys = typyPRISM.System(['A','B'])

        # ** populate system variables **
        
        PRISM = sys.createPRISM()

        PRISM.solve()

        sk = typyPRISM.calculate.structure_factor(PRISM)

        sk_BB = sk['B','B']
    
    '''
    
    if PRISM.totalCorr.space == Space.Real:
        PRISM.sys.domain.MatrixArray_to_fourier(PRISM.totalCorr)
        
    if PRISM.omega.space == Space.Real:
        PRISM.sys.domain.MatrixArray_to_fourier(PRISM.omega)
    
    structureFactor = (PRISM.totalCorr*PRISM.sys.density.pair + PRISM.omega)/PRISM.sys.density.site
    # structureFactor = PRISM.totalCorr + PRISM.omega
    
    return structureFactor
