#!python
from pyPRISM.core.Domain import Domain
from pyPRISM.core.Space import Space
from pyPRISM.closure.MolecularClosure import MolecularClosure
from pyPRISM.closure.PercusYevick import PercusYevick

from scipy.signal import fftconvolve
import numpy as np
from numpy import inf

class ReferenceMolecularPercusYevick(MolecularClosure):
    r'''Reference Molecular Percus Yevick (R-MPY) closure

    .. warning::

        This closure is not fully implemented. It should throw an error if a
        user attempts to use it.
    

    **Mathematial Definition**

        .. math:: 
            c_{\alpha,\beta}(r) = & \omega_{\alpha,\alpha}(r)*c^0_{\alpha,\beta}(r)*\omega_{\beta,\beta}(r) + \\
            & \omega_{\alpha,\alpha}(r)*[(\exp(-u_{\alpha,\beta}(r)) - 1.0) (1.0 + \gamma_{\alpha,\beta}(r))]*\omega_{\beta,\beta}(r) \\
            \gamma_{\alpha,\beta}(r) = & h_{\alpha,\beta}(r) - c_{\alpha,\beta}(r)

    
    **Variables Definitions**

        - :math:`A*B`
            Convolution integral between A and B

        - :math:`h_{\alpha,\beta}(r)` 
            Total correlation function value at distance :math:`r` between
            sites :math:`\alpha` and :math:`\beta`.
    
        - :math:`c_{\alpha,\beta}(r)`
            Direct correlation function value at distance :math:`r` between
            sites :math:`\alpha` and :math:`\beta`.

        - :math:`c^0_{\alpha,\beta}(r)`
            Referene of Direct correlation function value at distance :math:`r`
            between sites :math:`\alpha` and :math:`\beta`.
    
        - :math:`\omega_{\alpha,\beta}(r)`
            *Intra*-molecular correlation function value at distance :math:`r`
            between sites :math:`\alpha` and :math:`\beta`.
    
        - :math:`u_{\alpha,\beta}(r)`
            Non-hardcore portion of Interaction potential value at distance
            :math:`r` between sites :math:`\alpha` and :math:`\beta`.
    
    **Description**

        TBA

    
    References
    ----------
        Schweizer, K.S.; Yethiraj, Arun; Polymer reference interaction site
        model theory: New molecular closure for phase separating fluids and
        alloys, The Journal of Chemical Physics 98, 9053 (1993); doi:
        10.1063/1.464465

    '''
    def __init__(self,apply_hard_core=False):
        #raise NotImplementedError('Molecular closures are untested and not fully implemented.')
        
        self.name = "RMPY"
        self.potential = None
        self.value = None
        self.sigma = None
        self.apply_hard_core = apply_hard_core
        
        
    def __repr__(self):
        return '<MolecularClosure: ReferenceMolecularPercusYevick>'
    
    def calculate(self,domain,gamma,omega_k_i,omega_k_j,cr0,hk0,hk):
        r'''Calculate direct correlation function

        Arguments
        ---------
        gamma: np.ndarray
            array of :math:`\gamma` values used to calculate the direct
            correlation function; these are in real space

        omega1,omega2: np.ndarray
            array of :math:`\omega_{\alpha,\alpha}` or
            :math:`\omega_{\beta,\beta}` values used to calculate the direct
            correlation function; these are in fourier space
        
        '''
        
        r=domain.r

        assert self.potential is not None,'Potential for this closure is not set!'
        
        assert len(gamma) == len(self.potential),'Domain mismatch!'

        hr = Domain.to_real(domain,array=hk)

        # We need to set the potential for r<=sigma equal to 0 for the fft to work correctly
        # IMPORTANT: Use np.copy() to avoid modifying self.potential in place
        potential_calculation = np.copy(self.potential)
        mask = r<=self.sigma
        potential_calculation[mask]=0.0

        exp_potential_r = (np.exp(+potential_calculation) - 1.0) * ( hr + 1.0)
        exp_potential_k = Domain.to_fourier(domain,array=exp_potential_r)
        exp_potential_k = omega_k_i*exp_potential_k*omega_k_j
        exp_potential_r = Domain.to_real(domain,array=exp_potential_k)

        cr0_k = Domain.to_fourier(domain,array=cr0)        
        convoluted_cr0_k = omega_k_i*cr0_k*omega_k_j
        convoluted_cr0 = Domain.to_real(domain,array=convoluted_cr0_k)

        if self.apply_hard_core:
            self.value = -1 - gamma
            mask = r > self.sigma
            self.value[mask] = convoluted_cr0[mask] + exp_potential_r[mask]

        else:
           # self.value is the convoluted c(r)

            self.value = convoluted_cr0 + exp_potential_r
        
        return self.value

class RMPY(ReferenceMolecularPercusYevick):
    '''Alias of ReferenceMolecularPercusYevick'''
    pass
