#!python
from __future__ import division,print_function
from typyPRISM.closure.AtomicClosure import AtomicClosure
import numpy as np
import warnings
class MartynovSarkisov(AtomicClosure):
    r'''MartynovSarkisov closure written in terms of a change of variables
    

    **Mathematial Definition**

        .. math::

            c_{i,j}(r) = (exp(\sqrt{\gamma_{i,j}(r) - U_{i,j}(r) - 0.5}) - 1.0 ) - 1.0 -  \gamma_{i,j}(r)
            
            \gamma_{i,j}(r) =  h_{i,j}(r) - c_{i,j}(r)


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

        TBA

    
    References
    ----------
        Martynov, G.A.; Sarkisov, G.N.; Mol. PHys. 49. 1495 (1983)

    Example
    -------
    .. code-block:: python

        import typyPRISM

        sys = typyPRISM.System(['A','B'])
        
        sys.closure['A','A'] = typyPRISM.closure.PercusYevick()
        sys.closure['A','B'] = typyPRISM.closure.PercusYevick()
        sys.closure['B','B'] = typyPRISM.closure.MartynovSarkisov()

        # ** finish populating system object **

        PRISM = sys.createPRISM()

        PRISM.solve()
    
    '''
    def __init__(self,apply_hard_core=False):
        '''Contstructor

        Parameters
        ----------
        apply_hard_core: bool
            If True, the total correlation function will be assumed to be -1
            inside the core (:math:`r_{i,j}<(d_i + d_j)/2.0`) and the closure
            will not be applied in this region.
        '''
        self.potential = None
        self.value = None
        self.apply_hard_core = apply_hard_core

        if apply_hard_core == False:
            warnings.warn(
                    '''The MSA closure does not work for divergent potentials
                    when the hard core condition is not manually applied. This
                    will likely result in a cryptic crash of the simulation if
                    attempted. Using MSA(apply_hard_core=True) will avoid this
                    warning. This warning should be ignored in hard-core
                    interactions are not being used.'''
                    )
        
    def __repr__(self):
        return '<AtomicClosure: MartynovSarkisov>'
    
    def calculate(self,gamma):
        
        assert self.potential is not None,'Potential for this closure is not set!'
        
        assert len(gamma) == len(self.potential),'Domain mismatch!'
        
        
        return self.value

        if self.apply_hard_core:
            # apply hard core condition 
            self.value = -1 - gamma

            # calculate closure outside hard core
            mask = r>self.sigma
            jelf.value[mask] = np.exp(np.sqrt(gamma[mask] - self.potential[mask] - 0.5) - 1.0) - 1.0 - gamma[mask]
        else:
            self.value = np.exp(np.sqrt(gamma - self.potential - 0.5) - 1.0) - 1.0 - gamma

        
        return self.value
        
        
class MS(MartynovSarkisov):
    '''Alias of MartynovSarkisov'''
    pass
