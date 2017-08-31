#!python 
from __future__ import division,print_function
import numpy as np
from typyPRISM.core.PRISM import PRISM
from typyPRISM.core.MatrixArray import MatrixArray
from typyPRISM.core.PairTable import PairTable
from typyPRISM.core.ValueTable import ValueTable
from typyPRISM.core.Space import Space

class System:
    '''Primary class used to spawn PRISM calculations
    
    .. warning::
    
        The *intra*-molecular correlation functions (omega attribute)
        should be specified such that they are in Fourier space and such
        that their k->0 values approach the total number of sites in a 
        given molecule for the self (i==j) pairs.
    
    Attributes
    ----------
    types: list
        list of site types
        
    rank: int
        number of site types
    
    density: typyPRISM.core.ValueTable
        Table of site *number* density values
        
    potential: typyPRISM.core.PairTable
        Table of pair potentials between all site pairs in real space
        
    closure: typyPRISM.core.PairTable
        Table of closures between all site pairs
        
    omega: typyPRISM.core.PairTable
        Table of omega correlation functions in k-space
    
    domain: typyPRISM.core.Domain
        Domain object which specifies the Real and Fourier space 
        solution grid.
        
    kT: float
        Value of the thermal energy scale. Used to vary temperature and
        scale the potential energy functions.

    siteDensityMatrix: np.ndarray, size (rank,rank)
        Total site density for each pair. For i == j, the site_density =
        rho_i, for i != j site_density = rho_i + rho_j

    pairDensityMatrix: np.ndarray, size (rank,rank)
        Pair site density for each pair.  pair_density = rho_i * rho_j
    
    
    '''
    def __init__(self,types,kT=1.0):
        self.types = types
        self.rank  = len(types)
        self.kT = kT
        
        self.domain    = None
        self.density   = ValueTable(types,'density')
        self.potential = PairTable(types,'potential')
        self.closure   = PairTable(types,'closure')
        self.omega = PairTable(types,'omega')

        self.siteDensityMatrix = None
        self.sitePairMatrix = None
    
    def check(self):
        '''Make sure all values in the system are specified'''
        for table in [self.density,self.potential,self.closure,self.omega]:
            table.check()
        
        if self.domain is None:
            raise ValueError(('System has no domain! '
                              'User must instatiate and assign a domain to the system!'))
    def createDensityMatrices(self):
        '''See method name
        
        .. math::
        
            \rho^{pair}_{i,j} = \rho_i * \rho_j
            
        
            \rho^{site}_{i,j} = \rho_i + \rho_j, if i != j
            
            \rho^{site}_{i,j} = \rho_i         , if i = j
        '''
        siteDensityMatrix = np.zeros((self.rank,self.rank))
        pairDensityMatrix = np.zeros((self.rank,self.rank))
        for i,t1,rho1 in self.density:
            for j,t2,rho2 in self.density:
                if i>j:
                    continue
                    
                if i==j:
                    siteDensityMatrix[i,j] = rho1
                    pairDensityMatrix[i,j] = rho1 * rho2
                else:
                    siteDensityMatrix[i,j] = rho1 + rho2
                    siteDensityMatrix[j,i] = rho1 + rho2
                    
                    pairDensityMatrix[i,j] = rho1 * rho2
                    pairDensityMatrix[j,i] = rho1 * rho2
                    
        return siteDensityMatrix,pairDensityMatrix
            
    def createPRISM(self):
        '''Construct a fully specified PRISM object that can be solved'''
        self.check() #sanity check

        #create density
        self.siteDensityMatrix,self.pairDensityMatrix = self.createDensityMatrices()
        
        # Need to set the potential for each closure object
        for (i,j),(t1,t2),U in self.potential.iterpairs():
            self.closure[t1,t2].potential = U.calculate(self.domain.r) / self.kT

        return PRISM(self)
        
