#!python
from __future__ import division,print_function
from typyPRISM.closure.AtomicClosure import AtomicClosure
import numpy as np
class PercusYevick(AtomicClosure):
    r'''Percus Yevick closure evaluated in terms of a change of variables

    **Mathematial Definition**

        .. math:: c_{\alpha,\beta}(r) = (\exp(-u_{\alpha,\beta}(r)) - 1.0) (1.0 + \gamma_{\alpha,\beta}(r))

        .. math:: \gamma_{\alpha,\beta}(r) =  h_{\alpha,\beta}(r) - c_{\alpha,\beta}(r)

    **Variables Definitions**

        - :math:`h_{\alpha,\beta}(r)` 
            Total correlation function value at distance :math:`r` between
            sites :math:`\alpha` and :math:`\beta`.
    
        - :math:`c_{\alpha,\beta}(r)`
            Direct correlation function value at distance :math:`r` between
            sites :math:`\alpha` and :math:`\beta`.
    
        - :math:`u_{\alpha,\beta}(r)`
            Interaction potential value at distance :math:`r` between sites
            :math:`\alpha` and :math:`\beta`.
    

    **Description**

        The Percus-Yevick (PY) is derived by expanding the exponential of the
        direct correlation function, c, in powers of density shift from a
        refence state. See Hansen and McDonald for a full derivation.
        
        The change of variables is necessary in order to use potentials with
        hard cores in the computational setting. Written in the standard form,
        this closure diverges with divergent potentials, which makes it
        impossible to numerically solve. 

        This closure has been shown to be accurate for systems with hard cores
        (strongly repulsive at short distances) and when the potential is short
        ranged. 
    
    References
    ----------
        Hansen, J.P.; McDonald, I.R.; Theory of Simple Liquids; Chapter 4, Section 4; 
        4th Edition (2013), Elsevier

    Example
    -------
    .. code-block:: python

        import typyPRISM

        sys = typyPRISM.System(['A','B'])
        
        sys.closure['A','A'] = typyPRISM.closure.PercusYevick()
        sys.closure['A','B'] = typyPRISM.closure.PercusYevick()
        sys.closure['B','B'] = typyPRISM.closure.HypernettedChain()

        # ** finish populating system object **

        PRISM = sys.createPRISM()

        PRISM.solve()
    
    '''
    def __init__(self):
        self.potential = None
        self.value = None
        
    def __repr__(self):
        return '<AtomicClosure: PercusYevick>'
    
    def calculate(self,gamma):
        '''Calculate direct correlation function based on supplied :math:`\gamma`

        Arguments
        ---------
        gamma: np.ndarray
            array of :math:`\gamma` values used to calculate the direct
            correlation function
        
        '''
        
        assert self.potential is not None,'Potential for this closure is not set!'
        
        assert len(gamma) == len(self.potential),'Domain mismatch!'
        
        self.value = (np.exp(-self.potential)-1.0)*(1.0+gamma)
        
        return self.value
        
        
