import numpy as np
from typyPRISM.core.PRISM import PRISM
from typyPRISM.core.MatrixArray import MatrixArray
from typyPRISM.core.PairTable import PairTable
from typyPRISM.core.ValueTable import ValueTable
from typyPRISM.core.Space import Space

class System:
    '''Primary class used to spawn PRISM calculations
    
    .. warning::
    
        The *intra*-molecular correlation functions (intraMolCorr attribute)
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
        
    intraMolCorr: typyPRISM.core.PairTable
        Table of intramolecular correlation functions in k-space
    
    domain: typyPRISM.core.Domain
        Domain object which specifies the Real and Fourier space 
        solution grid.
    
    
    '''
    def __init__(self,types):
        self.types = types
        self.rank  = len(types)
        
        self.domain    = None
        self.density   = ValueTable(types,'density')
        self.potential = PairTable(types,'potential')
        self.closure   = PairTable(types,'closure')
        self.intraMolCorr = PairTable(types,'intraMolCorr')
    
    def check(self):
        '''Make sure all values in the system are specified'''
        for table in [self.density,self.potential,self.closure,self.intraMolCorr]:
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
        siteDensityMatrix,pairDensityMatrix = self.createDensityMatrices()
        
        
        # The intraMolCorr objects must be converted to arrays of the actual correlation
        # function values. 
        self.intraMolCorr.apply(lambda x: x.calculate(self.domain.k))
        
        # Next, the intraMolCorr table is converted to a MatrixArray so that we can easily
        # do operations during the PRISM solution
        intraMolCorr = self.intraMolCorr.exportToMatrixArray(space=Space.Fourier)
        
        # Finally, the correlation functions are scaled by the density matrix
        intraMolCorr *= siteDensityMatrix 
        
        # Need to set the intramolecular potential for each closure object
        r = self.domain.r
        for (i,j),(t1,t2),U in self.potential.iterpairs():
            self.closure[t1,t2].potential = U.calculate(r)
        
        args = []
        args.append(self.rank)
        args.append(self.domain)
        args.append(self.closure)
        args.append(intraMolCorr)
        args.append(pairDensityMatrix)
        args.append(siteDensityMatrix)
        return PRISM(*args)
        