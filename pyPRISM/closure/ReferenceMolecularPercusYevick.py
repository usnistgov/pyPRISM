#!python
from __future__ import division,print_function
from pyPRISM.closure.MolecularClosure import MolecularClosure
from pyPRISM.closure.PercusYevick import PercusYevick

from scipy.signal import fftconvolve
from scipy.optimize import fsolve
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

        TBA TG making edits

    
    References
    ----------
        Schweizer, K.S.; Yethiraj, Arun; Polymer reference interaction site
        model theory: New molecular closure for phase separating fluids and
        alloys, The Journal of Chemical Physics 98, 9053 (1993); doi:
        10.1063/1.464465

    '''
    def __init__(self,C0,apply_hard_core=False):
        r'''Contstructor

        Parameters
        ----------
        C0: MatrixArray
            MatrixArray of :math:`C_{\alpha,\alpha}_0(r)` values obtained for the solved
            athermal reference system
        
        apply_hard_core: bool
            If True, the total correlation function will be assumed to be -1
            inside the core (:math:`r_{i,j}<(d_i + d_j)/2.0`) and the closure
            will not be applied in this region.
        '''
        #raise NotImplementedError('Molecular closures are untested and not fully implemented.')

        self._potential = None
        self.value = None
        self._sigma = None
        #self.PY = PercusYevick(apply_hard_core=True)
        self.C0 = C0
        self.apply_hard_core=apply_hard_core
        
    def __repr__(self):
        return '<MolecularClosure: ReferenceMolecularPercusYevick>'


    @property
    def potential(self):
        return self._potential
    
    @property
    def sigma(self):
        return self._sigma

    @potential.setter
    def potential(self,value):
        self._potential =  value
        #self.PY.potential = value
    
    @sigma.setter
    def sigma(self,value):
        self._sigma =  value
        #self.PY.sigma = value
   
    def calculate(self,r,WCW,gamma):
        r'''Calculate direct correlation function

        Arguments
        ---------
        r: np.ndarray
            array of real-space values associated with :math:`\gamma`
        
        gamma: MatrixArray
            MatrixArray of :math:`\gamma` values used to calculate the direct
            correlation function

        WCW: MatrixArray
            MatrixArray of :math:`\Omega(r)*C(r)*\Omega(r)*` values 
            used to calculate the direct
            correlation function. NOTE: these need to be in real-space!
        
        '''
        
        assert self.potential is not None,'Potential for this closure is not set!'
        
        assert WCW.shape[0] == len(self.potential),'Domain mismatch!'
        
        self.value = np.zeros_like(self.potential)
        self.value_lo = np.zeros_like(self.potential)
        self.value_hi  = np.zeros_like(self.potential)
        if self.apply_hard_core:
            assert self.sigma is not None, 'If apply_hard_core=True, sigma parameter must be set!'

            # calculate closure inside hard core
            mask = r<self.sigma
            self.value_lo[mask] = (1.0-np.exp(0.0))*(1.0+WCW[mask]+gamma[mask])
            self.value_lo[mask] += self.C0[mask]
            # self.value_lo[mask] = -1.0-gamma[mask]
            
            # calculate closure outside hard core
            mask = r>self.sigma
            self.value_hi[mask] = (1.0-np.exp(self.potential[mask]))*(1.0+WCW[mask]+gamma[mask])
            self.value_hi[mask] += self.C0[mask]

            self.value = self.value_lo + self.value_hi
        else:
            raise AssertionError('Please specify apply_hard_core=True!')
        
        return self.value


class RMPY(ReferenceMolecularPercusYevick):
    '''Alias of ReferenceMolecularPercusYevick'''
    pass
