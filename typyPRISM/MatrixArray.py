
from itertools import product
import numpy as np

#See for fast inverse https://stackoverflow.com/q/11972102
class MatrixArray:
    '''A container for creating and interacting with arrays of matrices
    
    The primary data structure of MatrixArray is simply a 3D Numpy array 
    with the first dimension accessing each individual matrix in the array
    and the last two dimenions corresponding to the vertical and horizontal 
    index of each matrix element.
    
    The terminology *column* is used to refer to the set of values from
    all matrices in the array at a given matrix index pair. In Numpy slicing 
    parlance::
    
        column_11 = numpy_array[:,1,1]
        column_12 = numpy_array[:,1,2]
    
    
    Attributes
    ----------
    rank: int
        Number of rows/cols of each (square) matrix. For PRISM theory, this 
        also equal to the number of site types.
        
    length: int
        Number of matrices in array. For PRISM theory, this corresponds to
        the number of grid points in real- and Fourier-space i.e. Domain.size.
        
    data: float np.ndarray, size (length,rank,rank)
        Interface for specifying the MatrixArray data directly. If not given,
        all matrices will be set to zero. 
    '''
    __slots__ = ('rank','length','data')
    
    def __init__(self,length,rank,data=None):
        self.rank = rank
        self.length = length
                    
        if data is None:
            self.data = np.zeros((length,rank,rank))
        else:
            self.data = data
            
    def __repr__(self):
        return '<MatrixArray rank:{:d} length:{:d}>'.format(self.rank,self.length)
    
    def itercolumn(self):
        for i,j in product(range(self.rank),range(self.rank)):
            if i<=j: #upper triangle condition
                yield (i,j),self.data[:,i,j]
            
    def __setitem__(self,key,val):
        '''Column setter 
        
        Assumes all matrices are symmetric and enforces symmetry by
        setting both off diagonal elements. 
        '''
        type1,type2 = key
        self.data[:,type1,type2] = val
        if not (type1 == type2):
            self.data[:,type2,type1] = val
        
    def __getitem__(self,key):
        '''Column getter'''
        type1,type2 = key
        return self.data[:,type1,type2]
    
    def __mul__(self,other):
        '''Scalar or elementwise multiplication'''
        if type(other) is MatrixArray:
            data = self.data * other.data
        else:
            data = self.data * other
        return MatrixArray(self.rank,self.length,data=data)
    
    def __imul__(self,other):
        '''Scalar or elementwise multiplication'''
        if type(other) is MatrixArray:
            self.data *= other.data
        else:
            self.data *= other
        return self
            
    def __add__(self,other):
        if type(other) is MatrixArray:
            data = self.data + other.data
        else:
            data = self.data + other
        return MatrixArray(self.rank,self.length,data=data)
    
    def __iadd__(self,other):
        if type(other) is MatrixArray:
            self.data += other.data
        else:
            self.data += other
        return self
            
    def __sub__(self,other):
        if type(other) is MatrixArray:
            data = self.data - other.data
        else:
            data = self.data - other
        return MatrixArray(self.rank,self.length,data=data)
    
    def __isub__(self,other):
        if type(other) is MatrixArray:
            self.data -= other.data
        else:
            self.data -= other
        return self
            
    def invert(self,inplace=False):
        '''Perform matrix inversion on all matrices in the MatrixArray
        
        Parameters
        ----------
        inplace: bool
            If False, a new MatrixArray is returned, otherwise just
            update the internal data.
        '''
        if inplace:
            data = self.data
        else:
            data = np.copy(self.data)
            
        for i in range(self.length):
            data[i] = np.linalg.inv(self.data[i])
            
        if not inplace:
            return data
            
    def dot(self,other,inplace=False):
        ''' Matrix multiplication for each matrix in two MatrixArrays
        
        Parameters
        ----------
        other: object, MatrixArray
            Must be an object of MatrixArray type of the same length
            and dimension
            
        inplace: bool
            If False, a new MatrixArray is returned, otherwise just
            update the internal data.
        
        '''
        if inplace:
            self.data = np.einsum('lij,ljk->lik', self.data, other.data)
        else:
            data = np.einsum('lij,ljk->lik', self.data, other.data)
            return MatrixArray(self.rank,self.length,data=data)
        
        