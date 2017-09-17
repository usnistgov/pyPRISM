#!python
from __future__ import division,print_function
from typyPRISM.core.PairTable import PairTable
from typyPRISM.core.MatrixArray import MatrixArray
from typyPRISM.core.Space import Space
from typyPRISM.calculate.structure_factor import structure_factor
import numpy as np

def solvation_potential(PRISM,closure='HNC'):
    '''Calculate the pairwise decomposed medium-induced solvation potential
    
        
    Parameters
    ----------
    PRISM: typyPRISM.core.PRISM
        A **solved** PRISM object.

    closure: str ('PY' or 'HNC')
        closure used to derive the potential 

    
    Returns
    -------
    psi: typyPRISM.core.MatrixArray
        MatrixArray of all wavenumber dependent chi pairs indexed by tuple pairs
    
    '''
    
    assert PRISM.sys.rank>1,'the psi calculation is only valid for multicomponent systems'
    
    if PRISM.directCorr.space == Space.Real:
        PRISM.domain.MatrixArray_to_fourier(PRISM.directCorr)

    if PRISM.totalCorr.space == Space.Real:
        PRISM.sys.domain.MatrixArray_to_fourier(PRISM.totalCorr)
        
    if PRISM.omega.space == Space.Real:
        PRISM.sys.domain.MatrixArray_to_fourier(PRISM.omega)

    structureFactor = structure_factor(PRISM)#(PRISM.totalCorr*PRISM.sys.pairDensityMatrix + PRISM.omega)/PRISM.sys.siteDensityMatrix

    if closure == 'HNC':
        psi = PRISM.directCorr.dot(structureFactor).dot(PRISM.directCorr) * -PRISM.sys.kT 
    elif closure == 'PY':
        psi = PRISM.directCorr.dot(structureFactor).dot(PRISM.directCorr)
        psi.data = np.log(1 + psi.data) * -PRISM.sys.kT

    PRISM.sys.domain.MatrixArray_to_real(psi)

    return psi
