#!python

from __future__ import division,print_function
from typyPRISM.core.MatrixArray import MatrixArray
from typyPRISM.core.Space import Space
from typyPRISM.core.PairTable import PairTable
import numpy as np

def spinodal_condition(PRISM):
    '''Calculate the spinodal condition between pairs of components 

    This calculation is only exactly correct for a two component system. It's 
    basis is in the fact that the value 

    .. note:

        Schweizer, Curro, Thermodynamics of Polymer Blends,
        J. Chem. Phys., 1989 91 (8) 5059
        
    Parameters
    ----------
    PRISM: typyPRISM.core.PRISM.PRISM
        A **solved** PRISM object.
    
    Returns
    -------
    lambda: typyPRISM.core.PairTable
        Dictionary of all wavenumber dependent chi pairs indexed by tuple pairs
    
    '''
    
    assert PRISM.sys.rank>1,'The spinodal calculation is only valid for multicomponent systems'
    
    if PRISM.directCorr.space == Space.Real:
        PRISM.sys.domain.MatrixArray_to_fourier(PRISM.directCorr)

    if PRISM.omega.space == Space.Real:
        PRISM.sys.domain.MatrixArray_to_fourier(PRISM.omega)
        
    
    lam = PairTable(name='spinodal_condition',types=PRISM.sys.types)
    for i,t1 in enumerate(PRISM.sys.types):
        for j,t2 in enumerate(PRISM.sys.types):
            if i<j:

                omega_AA  = PRISM.omega[t1,t1]
                omega_AB  = PRISM.omega[t1,t2]
                omega_BB  = PRISM.omega[t2,t2]

                C_AA = PRISM.directCorr[t1,t1]
                C_AB = PRISM.directCorr[t1,t2]
                C_BB = PRISM.directCorr[t2,t2]

                rho_AA = PRISM.sys.siteDensityMatrix[i,i]
                rho_AB = PRISM.sys.siteDensityMatrix[i,j]
                rho_BB = PRISM.sys.siteDensityMatrix[j,j]

                value  = +1
                value += -1*C_AA * rho_AA * omega_AA
                value += -2*C_AB * rho_AB * omega_AB
                value += -1*C_BB * rho_BB * omega_BB
                value += +C_AB*C_AB * rho_AB*rho_AB * omega_AB*omega_AB
                value += -C_AA*C_BB * rho_AB*rho_AB * omega_AB*omega_AB
                value += -C_AB*C_AB * rho_AA*rho_BB * omega_AA*omega_BB
                value += +C_AA*C_BB * rho_AA*rho_BB * omega_AA*omega_BB

                
                lam[t1,t2] = value
                  
        
    
    return lam
