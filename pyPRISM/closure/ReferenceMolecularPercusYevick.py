#!python
from __future__ import division,print_function
from pyPRISM.closure.MolecularClosure import MolecularClosure
from pyPRISM.closure.PercusYevick import PercusYevick

from scipy.signal import fftconvolve
import numpy as np

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
    def __init__(self,C0):
        raise NotImplementedError('Molecular closures are untested and not fully implemented.')

        self._potential = None
        self.value = None
        self.PY = PercusYevick()
        self.C0 = C0
        
    def __repr__(self):
        return '<MolecularClosure: ReferenceMolecularPercusYevick>'


    @property
    def potential(self):
        return self._potential

    @potential.setter
    def potential(self,value):
        self._potential =  value
        self.PY.potential = value
    
    def calculate(self,gamma,omega1,omega2):
        r'''Calculate direct correlation function

        Arguments
        ---------
        gamma: np.ndarray
            array of :math:`\gamma` values used to calculate the direct
            correlation function

        omega1,omega2: np.ndarray
            array of :math:`\omega_{\alpha,\alpha}` or
            :math:`\omega_{\beta,\beta}` values used to calculate the direct
            correlation function
        
        '''
        
        assert self.potential is not None,'Potential for this closure is not set!'
        
        assert len(gamma) == len(self.potential),'Domain mismatch!'

        
        value = self.C0 + self.PY.calculate(gamma)

        self.value = fftconvolve(fftconvolve(omega1,value,mode='same'),omega2,mode='same')
        
        return self.value
