from typyPRISM.core.MatrixArray import MatrixArray
from typyPRISM.core.Space import Space
import numpy as np

class IdentityMatrixArray(MatrixArray):
    '''Specialization of MatrixArray for Identity Matrices '''
    __slots__ = ('rank','length','data','space')
    
    def __init__(self,length,rank,data=None,space=None):
        self.rank = rank
        self.length = length
        
        if data is None:
            self.data = np.zeros((length,rank,rank))
            for i in range(rank):
                self.data[:,i,i] = 1.0
        else:
            self.data = data
            
        if space is None:
            self.space = Space.Real
        else:
            self.space = space
        