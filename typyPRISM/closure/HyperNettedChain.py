#!python
from __future__ import division,print_function
from typyPRISM.closure.AtomicClosure import AtomicClosure
import numpy as np
class HyperNettedChain(AtomicClosure):
    r'''HyperNettedChain closure written in terms of a change of variables

    **Mathematial Definition**

        .. math:: c_{\alpha,\beta}(r) = exp(\gamma_{\alpha,\beta}(r)-U_{\alpha,\beta}(r)) - 1.0 -  \gamma_{\alpha,\beta}(r)

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

        The Hypernetted Chain Closure (HNC) is derived by expanding the the
        direct correlation function, :math:`c(r)`, in powers of density shift
        from a refence state. See Hansen and McDonald for a full derivation.
        
        The change of variables is necessary in order to use potentials with
        hard cores in the computational setting. Written in the standard form,
        this closure diverges with divergent potentials, which makes it
        impossible to numerically solve. 

        Compared to the PercusYevick closure, the HNC closure is a more
        accurate approximation of the full expression for the direct
        correlation function. Depsite this, it can produce inaccurate,
        long-range fluctuations that make it difficult to employ in
        phase-separating systems. The HNC closure performs well for systems
        where there is a disparity in site diameters and is typically used for
        the larger site. 
    
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
        return '<AtomicClosure: HyperNettedChain>'
    
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
        
        self.value = np.exp(gamma - self.potential) - 1.0 - gamma
        
        return self.value
        
        
