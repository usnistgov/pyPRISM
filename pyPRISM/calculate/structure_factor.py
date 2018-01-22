#!python
from __future__ import division,print_function
from pyPRISM.core.Space import Space

def structure_factor(PRISM,normalize=True):
    r'''Calculate the structure factor from a PRISM object
    
        
    Parameters
    ----------
    PRISM: pyPRISM.core.PRISM
        A **solved** PRISM object.

    normalize: bool
        normalize the structure factor by the site density
    
    Returns
    -------
    structureFactor: pyPRISM.core.MatrixArray
        The full MatrixArray of structure factors

        
    **Mathematical Definition**


    .. math::

        \hat{s}_{\alpha,\beta}(k) = \rho^{site}_{\alpha,\beta} \hat{\omega}_{\alpha,\beta}(k) + \rho^{pair}_{\alpha,\beta} \hat{h}_{\alpha,\beta}(k)

    .. math::

        \hat{s}_{\alpha,\beta}^{norm}(k) = \hat{s}_{\alpha,\beta}(k) / \rho^{site}_{\alpha,\beta}  

    
    **Variable Definitions**

        - :math:`\hat{\omega}_{\alpha,\beta}(k)`
            Intra-molecular correlation function between sites :math:`\alpha`
            and :math:`\beta` at a wavenumber :math:`k`

        - :math:`\hat{h}_{\alpha,\beta}(k)`
            Total correlation function between sites :math:`\alpha` and
            :math:`\beta` at a wavenumber :math:`k`

        - :math:`\rho^{site}_{\alpha,\beta}`, :math:`\rho^{pair}_{\alpha,\beta}`
            Sitewise and pairwise densities for sites :math:`\alpha` and
            :math:`\beta`. See :class:`pyPRISM.core.Density` for details. 

    **Description**

        The structure factor (:math:`\hat{s}_{\alpha,\beta}(k)`) is a 
        Fourier-space representation of the structural correlations between
        sites :math:`\alpha` and :math:`\beta`. The :math:`\hat{s}_{\alpha,\beta}(k)`
        can be related to the real-space pair correlation function through a 
        Fourier transform. In the PRISM formalism, the 
        :math:`\hat{s}_{\alpha,\beta}(k)` can be calculated as the sum of the 
        Fourier-space intra-molecular and total correlation functions, as 
        shown above. 


    .. warning::

        Passing an unsolved PRISM object to this function will still produce
        output based on the default values of the attributes of the PRISM
        object.
    
    
    References
    ----------
    #. Chandler, D., Introduction to Modern Statistical Mechanics, 
       Oxford U. Press, New York, 1987 [`link
       <https://books.google.com/books/about/Introduction_to_Modern_Statistical_Mecha.html?id=3taTh5D-CDsC>`__]

    #. Schweizer, Curro, Integral equation theory of the structure and
       thermodynamics of polymer blends, J. Chem. Phys., 1989 91 (8) 5059 [`link
       <https://doi.org/10.1063/1.457598>`__]


    Example
    -------
    .. code-block:: python

        import pyPRISM

        sys = pyPRISM.System(['A','B'])

        # ** populate system variables **
        
        PRISM = sys.createPRISM()

        PRISM.solve()

        sk = pyPRISM.calculate.structure_factor(PRISM)

        sk_BB = sk['B','B']
    
    '''
    
    if PRISM.totalCorr.space == Space.Real:
        PRISM.sys.domain.MatrixArray_to_fourier(PRISM.totalCorr)
        
    if PRISM.omega.space == Space.Real:
        PRISM.sys.domain.MatrixArray_to_fourier(PRISM.omega)
    
    structureFactor = (PRISM.totalCorr*PRISM.sys.density.pair + PRISM.omega)/PRISM.sys.density.site
    # structureFactor = PRISM.totalCorr + PRISM.omega
    
    return structureFactor
