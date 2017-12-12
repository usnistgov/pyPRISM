#!python
from __future__ import division,print_function
from typyPRISM.closure.AtomicClosure import AtomicClosure
import numpy as np
import warnings 
class MeanSphericalApproximation(AtomicClosure):
    r'''Mean Spherical Approximation closure evaluated in terms of a change of variables

    **Mathematial Definition**

        .. math:: c_{\alpha,\beta}(r) = -u_{\alpha,\beta}(r)


    **Variables Definitions**

        - :math:`c_{\alpha,\beta}(r)`
            Direct correlation function value at distance :math:`r` between
            sites :math:`\alpha` and :math:`\beta`.
    
        - :math:`u_{\alpha,\beta}(r)`
            Interaction potential value at distance :math:`r` between sites
            :math:`\alpha` and :math:`\beta`.
    

    **Description**
        
        The Mean Spherical Approximation (MSA) closure assumes an interaction
        potential that contains a hard-core interaction and a tail interaction.
        See Hansen and McDonald for a derivation and discussion of this closure.
        
        The change of variables is necessary in order to use potentials with
        hard cores in the computational setting. Written in the standard form,
        this closure diverges with divergent potentials, which makes it
        impossible to numerically solve. 
        
        The MSA does a good job of describing the properties of the square-well 
        fluid, and allows for the analytical solution of the PRISM/RISM 
        equations for some systems. The MSA closure reduces to the PercusYevick 
        closure if the tail is ignored.

    
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
        self.sigma = None
        self.apply_hard_core = apply_hard_core

        if apply_hard_core == False:
            warnings.warn(
                    '''The MSA closure does not work for divergent potentials
                    when the hard core condition is not manually applied. This
                    will likely result in a cryptic crash of the simulation if
                    attempted. Using MSA(apply_hard_core=True) will avoid this
                    warning. This warning should be ignored in hard-core
                    interactions are not being used.''')

        
    def __repr__(self):
        return '<AtomicClosure: MeanSphericalApproximation>'
    
        
    def calculate(self,r,gamma):
        '''Calculate direct correlation function based on supplied :math:`\gamma`

        Arguments
        ---------
        r: np.ndarray
            array of real-space values associated with :math:`\gamma`

        gamma: np.ndarray
            array of :math:`\gamma` values used to calculate the direct
            correlation function
        
        '''
        
        assert self.potential is not None,'Potential for this closure is not set!'
        
        assert len(gamma) == len(self.potential),'Domain mismatch!'
        
        if self.apply_hard_core:
            # apply hard core condition 
            self.value = -1 - gamma

            # calculate closure outside hard core
            mask = r>self.sigma
            self.value[mask] = -self.potential[mask]
        else:
            self.value = -self.potential

        
        return self.value

class MSA(MeanSphericalApproximation):
    '''Alias of MeanSphericalApproximation'''
    pass
