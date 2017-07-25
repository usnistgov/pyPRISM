from typyPRISM.Space import Space
from typyPRISM.MatrixArray import MatrixArray
from typyPRISM.IdentityMatrixArray import IdentityMatrixArray
import numpy as np

class PRISM:
    '''Primary container for a PRISM problem and solution
    
    Each typyPRISM.PRISM object serves as an encapsulation 
    of a fully specified PRISM problem including all inputs
    needed for the calculation and the functional which 
    the will be numerically minimized. After minimization,
    the PRISM object should also contain all basic correlation
    functions and (in the future) methods for calculating 
    thermodynamic quanities based on them. 
    
    Attributes
    ----------
    domain: typyPRISM.Domain
        The Domain object fully specifies the real- and Fourier-
        space solution grids.
    
    directCorr: typyPRISM.MatrixArray
        The direct correlation function for all pairs of sites
        
    intraCorr: typyPRISM.MatrixArray
        The intra-molecular correlation function for all pairs 
        of sites. This is often shown as $\Omega$ in the PRISM 
        literature and is identical to what those in the scattering 
        fields would call a "form factor".
        
    pairCorr: typyPRISM.MatrixArray
        The pair correlation function for all pairs of sites. Also
        commonly refered to as the radial distribution functions.
    
    totalCorr: typyPRISM.MatrixArray
        The total correlation function is simply pair correlation 
        function y-shifted by 1.0 i.e. totalCorr = pairCorr - 1.0
        
    potential: typyPRISM.MatrixArray
        Interaction potentials for all pairs of sites
        
    GammaIn,GammaOut: typyPRISM.MatrixArray
        Primary inputs and outputs of the PRISM functional. Gamma is
        defined as "totalCorr - directCorr" (in Fourier space) and
        results from a change of variables used to remove divergences
        in the closure relations. 
    
    OC,IOC,I,etc: typyPRISM.MatrixArray
        Various MatrixArrays used as intermediates in the PRISM functional. 
        These arrays are pre-allocated and stored for efficiency. 
    
    x,y: float np.ndarray
        Current inputs and outputs of the cost function
    
    Methods
    -------
    funk:
        Primary cost function used to define the criteria of a "converged"
        PRISM solution. The numerical solver will be given this function 
        and will attempt to find the inputs (self.x) that make the outputs
        (self.y) as close to zero as possible. 
        
        
    '''
    __slots__ = (
                 'rank',
                 'domain',
                 'directCorr',
                 'intraCorr',
                 'pairCorr',
                 'totalCorr',
                 'GammaIn',
                 'GammaOut',
                 'potential',
                 'OC',
                 'IOC',
                 'I',
                 'cost',
                 'r',
                 'x',
                 'y',
                 'pairDensity',
                )
    def __init__(self,rank,domain,potential,intraCorr,pairDensity):
        self.domain = domain
        self.r = domain.r.reshape((-1,1,1)) # reshape to make Numpy broadcast correctly down the columns
        self.rank = rank
        
        self.potential = potential
        self.intraCorr  = intraCorr
        self.x = np.zeros(rank*rank*domain.length)
        self.y = np.zeros(rank*rank*domain.length)
        
        # Spaces are set based on when they are used in self.funk(...). In some cases,
        # this is redundant because these array's will be overwritten with copies and
        # then their space will be inferred from their parent MatrixArrays
        self.directCorr = MatrixArray(length=domain.length,rank=rank,space=Space.Real)
        self.pairCorr   = MatrixArray(length=domain.length,rank=rank,space=Space.Real)
        self.totalCorr  = MatrixArray(length=domain.length,rank=rank,space=Space.Fourier)
        self.GammaIn    = MatrixArray(length=domain.length,rank=rank,space=Space.Real)
        self.GammaOut   = MatrixArray(length=domain.length,rank=rank,space=Space.Real)
        self.OC         = MatrixArray(length=domain.length,rank=rank,space=Space.Fourier)
        self.I          = IdentityMatrixArray(length=domain.length,rank=rank,space=Space.Fourier)
        
        self.pairDensity = pairDensity
        
    def __repr__(self):
        return '<PRISM length:{} rank:{}>'.format(domain.length,rank)
        
    def funk(self,x):
        '''Cost function 
        
        There are likely several cost functions that could be imagined using
        the PRISM equations. In this case we formulate a self-consistent 
        formulation where we expect the input of the PRISM equations to be
        identical to the output. 
        
        '''
        self.x = x #store input
        
        # The np.copy is important otherwise x saves state between calls to
        # this function.
        self.GammaIn.data = np.copy(x.reshape((-1,self.rank,self.rank)))
        self.GammaIn     /= self.r
        
        # directCorr is calculated directly in Real space but immediately 
        # inverted to Fourier space. We must reset this from the last loop.
        self.directCorr.space = Space.Real 
        for (i,j),G in self.GammaIn.itercolumn():
            self.directCorr[i,j] = (np.exp(-self.potential[i,j])-1.0)*(1.0+G)
            
        self.domain.MatrixArray_to_fourier(self.directCorr)
        
        self.OC = self.intraCorr @ self.directCorr
        self.IOC = self.I - self.OC
        self.IOC.invert(inplace=True)
        
        self.totalCorr  = self.IOC @ self.OC @ self.intraCorr
        self.totalCorr /= self.pairDensity
        
        self.GammaOut  = self.totalCorr - self.directCorr
        
        self.domain.MatrixArray_to_real(self.GammaOut)
        
        self.y = self.r*(self.GammaOut.data - self.GammaIn.data)
        
        return self.y.reshape((-1,))
    def pair_correlation_function(self):
        '''Calculate the pair correlation function
        
        After convergence, the stored total correlation function MatrixArray
        (PRISM.totalCorr) can be Fourier transformed and 
        
        '''
        
        if self.totalCorr.space == Space.Fourier:
            domain.MatrixArray_to_real(self.totalCorr)
        
        self.pairCorr.data = np.copy(self.totalCorr.data) + 1.0
        
        return self.pairCorr
        