#!python
from __future__ import division,print_function
from pyPRISM.omega.Omega import Omega
import numpy as np


class ABDiblockFreelyJointedChain(Omega):
    r'''Intra-molecular correlation function describing correlations
    between unlike monomers in a freely-jointed A-B diblock polymer

    **Mathematical Definition**

    .. math::
    
        \hat{\omega}_{AB}(k) = \frac{E}{(N_A+N_B)(1-E)^2}(1-E^{N_A})(1-E^{N_B})

    .. math::
         
         E = \frac{\sin(k l)}{k l}


    **Variable Definitions**

        - :math:`\hat{\omega}_{AB}(k)` 
            *intra*-molecular correlation function at wavenumber :math:`k` for
            unlike monomer types A and B in an A-B diblock polymer

        - :math:`N_A` or :math:`N_B`
            number of repeat units in the A or B blocks
 
        - :math:`l`
            bond-length


    **Description**
        
        This expression describes the A-B correlations in the special case
        of an A-B diblock polymer where the A and B monomers are the same size
        and have the same bond length, and the individual blocks are treated
        as ideal freely-jointed chains.

    References
    ----------
    #. David, E.F.; Schweizer, K.S.; Integral Equation Theory of Block Copolymer
       Liquids II: Numerical results for finite hard-core diameter chains,
       J. Chem. Phys, 1994, 100 (10), pp 7784
       [`link <https://aip.scitation.org/doi/pdf/10.1063/1.466821>`__]

    Example
    -------
    .. code-block:: python

        import pyPRISM
        import numpy as np
        import matplotlib.pyplot as plt

        #calculate Fourier space domain and omega values
        domain = pyPRISM.domain(dr=0.1,length=1000)
        omega  = pyPRISM.omega.ABDiblockFreelyJointedChain(N_A=50,N_B=50,l=1.0)
        x = domain.k
        y = omega.calculate(x)

        #plot using matplotlib
        plt.plot(x,y)
        plt.gca().set_xscale("log", nonposx='clip')
        plt.gca().set_yscale("log", nonposy='clip')

        plt.show()
	
	#define a PRISM system and set omega(k) for type A
	sys = pyPRISM.System(['A','B'],kT=1.0)
	sys.domain = pyPRISM.Domain(dr=0.1,length=1024)
        sys.omega['A','B']  = pyPRISM.omega.ABDiblockFreelyJointedChain(N_A=50,N_B=50,l=1.0)

    
    '''
    def __init__(self,N_A,N_B,l):
        r'''Constructor
        
        Arguments
        ---------
        N_A: float
            number of monomers/sites in Freely-jointed block A
        
        N_B: float
            number of monomers/sites in Freely-jointed block B  
            
        l: float
            bond length
        '''
        self.Alength = self.N_A = N_A
        self.Blength = self.N_B = N_B
        self.l = l
        self.value = None
        
    def __repr__(self):
        return '<Omega: ABDiblockFreelyJointedChain>'
    
    def calculate(self,k):
        '''Return value of :math:`\hat{\omega}` at supplied :math:`k`

        Arguments
        ---------
        k: np.ndarray
            array of wavenumber values to calculate :math:`\omega` at
        
        '''
        E = np.sin(k*self.l)/(k*self.l)
        N_A = self.N_A
        N_B = self.N_B
        self.value = E/((N_A+N_B)*(1.0-E)**2.0)*(1.0-E**N_A)*(1.0-E**N_B)
        return self.value
        
        
class ABDiblockFJC(ABDiblockFreelyJointedChain):
    '''Alias of ABDiblockFreelyJointedChain'''
    pass
