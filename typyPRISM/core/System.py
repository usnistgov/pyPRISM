#!python 
from __future__ import division,print_function
import numpy as np
from typyPRISM.core.PRISM import PRISM
from typyPRISM.core.MatrixArray import MatrixArray
from typyPRISM.core.PairTable import PairTable
from typyPRISM.core.ValueTable import ValueTable
from typyPRISM.core.Space import Space
from typyPRISM.core.Density import Density

from typyPRISM.closure.AtomicClosure import AtomicClosure
from typyPRISM.closure.MolecularClosure import MolecularClosure

class System:
    '''Primary class used to spawn PRISM calculations

    **Description**

        The system object contains tables that fully describe a system to be
        simulated. This includes the domain definition, all site densities,
        site diameters, interaction potentials, intra-molecular correlation
        functions (:math:`\hat{\omega}(k)`), and closures. This class also
        contains a convenience function for spawning a PRISM object. 
    
    
    Example
    -------
    .. code-block:: python

        import typyPRISM

        sys = typyPRISM.System(['A','B'])
        
        sys.domain = typyPRISM.Domain(dr=0.1,length=1024)

        sys.density['A'] = 0.1
        sys.density['B'] = 0.75

        sys.diameter[sys.types] = 1.0
        
        sys.closure[sys.types,sys.types] = typyPRISM.closure.PercusYevick()

        sys.potential[sys.types,sys.types] = typyPRISM.potential.HardSphere()
        
        sys.omega['A','A'] = typyPRISM.omega.SingleSite()
        sys.omega['A','B'] = typyPRISM.omega.NoIntra()
        sys.omega['B','B'] = typyPRISM.omega.Gaussian(sigma=1.0,length=10000)
        
        PRISM = sys.createPRISM()

        PRISM.solve()

    '''
    def __init__(self,types,kT=1.0):
        r'''
        Arguments
        ---------
        types: list
            Lists of the site types that define the system

        kT: float
            Thermal temperature where k is the Boltzmann constant and T
            temperature. This is typicaly specified in reduced units where
            :math:`k_{B}=1.0`.


        Attributes
        ----------
        types: list
            List of site types
            
        rank: int
            Number of site types
        
        density: typyPRISM.Density
            Container for all density values
            
        potential: typyPRISM.PairTable
            Table of pair potentials between all site pairs in real space
            
        closure: typyPRISM.PairTable
            Table of closures between all site pairs
            
        omega: typyPRISM.PairTable
            Table of omega correlation functions in k-space
        
        domain: typyPRISM.Domain
            Domain object which specifies the Real and Fourier space 
            solution grid.
            
        kT: float
            Value of the thermal energy scale. Used to vary temperature and
            scale the potential energy functions.

        diameter: typyPRISM.ValueTable
            Site diameters. Note that these are not passed to potentials and it
            is up to the user to set sane \sigma values that match these 
            diameters. 
        '''

        self.types = types
        self.rank  = len(types)
        self.kT = kT
        
        self.domain    = None
        self.diameter  = ValueTable(types,'diameter')
        self.density   = Density(types)
        self.potential = PairTable(types,'potential')
        self.closure   = PairTable(types,'closure')
        self.omega = PairTable(types,'omega')

    def check(self):
        '''Is everything in the system specified?

        Raises
        ------
        ValueError if all values are not set
        
        '''
        for table in [self.density,self.potential,self.closure,self.omega,self.diameter]:
            table.check()
        
        if self.domain is None:
            raise ValueError(('System has no domain! '
                              'User must instatiate and assign a domain to the system!'))
    def createPRISM(self):
        '''Construct a fully specified PRISM object that can be solved'''
        self.check() #sanity check
        
        return PRISM(self)
        
