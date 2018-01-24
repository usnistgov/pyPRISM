#!python
from __future__ import division,print_function
from pyPRISM.core.PairTable import PairTable
from pyPRISM.core.MatrixArray import MatrixArray
from pyPRISM.core.Space import Space
from pyPRISM.calculate.structure_factor import structure_factor
import numpy as np

def solvation_potential(PRISM,closure='HNC'):
    r'''Calculate the pairwise decomposed medium-induced solvation potential
    
        
    Parameters
    ----------
    PRISM: pyPRISM.core.PRISM
        A **solved** PRISM object.

    closure: str ('PY' or 'HNC')
        closure used to derive the potential 

    
    Returns
    -------
    psi: pyPRISM.core.MatrixArray
        MatrixArray of the *Real-space* solvation potentials


    **Mathematical Definition**

    .. math::

        \text{PY: } \Delta \hat{\Psi}^{PY}(k) = - k_B T \ln(1 + \hat{C}(k)\hat{S}(k)\hat{C}(k))

    .. math::

        \text{HNC: } \Delta \hat{\Psi}^{HNC}(k) = - k_B T \hat{C}(k)\hat{S}(k)\hat{C}(k)

    
    **Variable Definitions**

        - :math:`\Delta \hat{\Psi}^{PY}`, :math:`\Delta \hat{\Psi}^{HNC}`
            Percus-Yevick and Hypernetted Chain derived pairwise decomposed
            solvation potentials, each described as a  :class:`.MatrixArray`.
            This implies that the multiplication in the above equation is
            actually *matrix* multiplication and the individual solvation
            potentials are extracted as curves of the MatrixArrays. Note that
            the solvation potential MatrixArrays are inverted back to
            Real-space for use. 

        - :math:`\hat{C}(k)`
            Direct correlation function :class:`.MatrixArray` at a wavenumber :math:`k`

        - :math:`\hat{S}(k)`
            Structure factor :class:`.MatrixArray` at a wavenumber :math:`k`

        - :math:`k_B T`
            Thermal temperature written as the product of the Boltzmann
            constant and temperature.

    **Description**

        The solvation potential (:math:`\Delta \hat{\Psi}`) mathematically
        describes how a given surrounding medium perturbs the site-site pairwise
        interactions of a molecule.

        This calculation is the foundation of the Self-Consistent PRISM
        formalism. See :ref:`SCPRISM` for more information.

    .. warning::

        Passing an unsolved PRISM object to this function will still produce
        output based on the default values of the attributes of the PRISM
        object.
    
    References
    ----------

    #. Grayce, Schweizer, Solvation potentials for macromolecules, J. Chem.
       Phys., 1994 100 (9) 6846 [`link <https://doi.org/10.1063/1.467044>`__]
    
    #. Schweizer, Honnell, Curro, Reference interaction site model theory of
       polymeric liquids: Self-consistent formulation and nonideality effects in
       dense solutions and melts, J. Chem. Phys., 1992 96 (4) 3211 [`link
       <https://doi.org/10.1063/1.461965>`__]

    Example
    -------
    .. code-block:: python

        import pyPRISM

        sys = pyPRISM.System(['A','B'])

        # ** populate system variables **
        
        PRISM = sys.createPRISM()

        PRISM.solve()

        psi = pyPRISM.calculate.solvation_potential(PRISM)

        psi_BB = psi['B','B']
    
    '''
    
    assert PRISM.sys.rank>1,'the psi calculation is only valid for multicomponent systems'
    
    if PRISM.directCorr.space == Space.Real:
        PRISM.domain.MatrixArray_to_fourier(PRISM.directCorr)

    if PRISM.totalCorr.space == Space.Real:
        PRISM.sys.domain.MatrixArray_to_fourier(PRISM.totalCorr)
        
    if PRISM.omega.space == Space.Real:
        PRISM.sys.domain.MatrixArray_to_fourier(PRISM.omega)

    structureFactor = structure_factor(PRISM)
    #(PRISM.totalCorr*PRISM.sys.pairDensityMatrix + PRISM.omega)/PRISM.sys.siteDensityMatrix

    if closure == 'HNC':
        psi = PRISM.directCorr.dot(structureFactor).dot(PRISM.directCorr) * -PRISM.sys.kT 
    elif closure == 'PY':
        psi = PRISM.directCorr.dot(structureFactor).dot(PRISM.directCorr)
        psi.data = np.log(1 + psi.data) * -PRISM.sys.kT

    PRISM.sys.domain.MatrixArray_to_real(psi)

    return psi
