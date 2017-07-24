import numpy as np
from typyPRISM.MatrixArray import MatrixArray

class IdentityMatrixArray(MatrixArray):
    '''Specialization of MatrixArray for Identity Matrices '''
    __slots__ = ('rank','length','data')
    
    def __init__(self,length,rank,data=None):
        self.rank = rank
        self.length = length
        
        if data is None:
            self.data = np.zeros((length,rank,rank))
            for i in range(rank):
                self.data[:,i,i] = 1.0
        else:
            self.data = data
        