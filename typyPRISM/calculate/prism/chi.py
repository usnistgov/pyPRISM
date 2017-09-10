#!python
from __future__ import division,print_function
from typyPRISM.core.PairTable import PairTable
from typyPRISM.core.MatrixArray import MatrixArray
from typyPRISM.core.Space import Space
import warnings
import numpy as np

COMPONENT_WARNING = '''
This calculate was derived for a two component system. It is often the case that
these calculations can be generalized for pairs of sites withing multicomponent 
systems. We caution the user when interpreting the data from this calculation 
for more than two components. 
'''

def chi(PRISM):
    '''Calculate the wavenumber-dependent effective interaction parameter (chi)
    
    .. math::
        
        \chi(k)  = 0.5 * \rho * (\hat{C}_{AA}(k) + \hat{C}_{BB}(k) - 2* + \hat{C}_{AB}(k))
        
    Parameters
    ----------
    PRISM: typyPRISM.core.PRISM
        A **solved** PRISM object.
    
    Returns
    -------
    chi: typyPRISM.core.PairTable
        PairTable of all wavenumber dependent chi pairs indexed by tuple pairs
    
    '''
    
    assert PRISM.sys.rank>1,'The chi calculation is only valid for multicomponent systems'

    if PRISM.sys.rank!=2:
        warnings.warn(COMPONENT_WARNING)
    
    if PRISM.directCorr.space == Space.Real:
        PRISM.domain.MatrixArray_to_fourier(PRISM.directCorr)
        
    
    chi = PairTable(name='chi',types=PRISM.sys.types)
    for i,t1 in enumerate(PRISM.sys.types):
        for j,t2 in enumerate(PRISM.sys.types):
            if i<j:
                C_AA = PRISM.directCorr[t1,t1]
                C_AB = PRISM.directCorr[t1,t2]
                C_BB = PRISM.directCorr[t2,t2]

                v_A = 4.0/3.0 * np.pi * (PRISM.sys.diameter[t1]/2.0)**(3.0)
                v_B = 4.0/3.0 * np.pi * (PRISM.sys.diameter[t2]/2.0)**(3.0)

                rho_A = PRISM.sys.density[t1]
                rho_B = PRISM.sys.density[t2]

                phi_A = rho_A/(rho_A + rho_B)
                phi_B = rho_B/(rho_A + rho_B)

                R = v_A/v_B
                
                chi[t1,t2] = (R**(-0.5)*phi_A + R**(0.5)*phi_B)**(-1.0)*0.5*PRISM.sys.density.total*(R**(-1.0) * C_AA + R*C_BB - 2*C_AB)
                
    return chi
