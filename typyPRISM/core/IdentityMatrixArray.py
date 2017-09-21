#!python
from typyPRISM.core.MatrixArray import MatrixArray
from typyPRISM.core.Space import Space
import numpy as np

class IdentityMatrixArray(MatrixArray):
    '''Specialization of MatrixArray which is initialized with Identity matrices'''
    
    def __init__(self,length,rank,data=None,space=None,types=None):
        super(IdentityMatrixArray,self).__init__(length=length,rank=rank,space=space,types=types)

        self.data = np.zeros((length,rank,rank))
        for i in range(rank):
            self.data[:,i,i] = 1.0
        
