#!python
from typyPRISM.core.Space import Space
from itertools import product
import numpy as np

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
        
    types: list, *optional*
        List of semantic types that can be used to reference data via the 
        getByTypes method. These types will be output by the itercolumn
        method as well. If not supplied, integer types will be generated.
        
    data: float np.ndarray, size (length,rank,rank)
        Interface for specifying the MatrixArray data directly. If not given,
        all matrices will be set to zero. 
    
    space: typyPRISM.Space
        Enumerated value tracking whether the array represents real or Fourier
        spaced data. As we will be transferring arrays to and from these spaces,
        it's important for safety that we track this.
    '''
    # __slots__ = ('rank','length','data','space')
    
    SpaceError = "Attempting MatrixArray math in non-matching spaces"
    
    def __init__(self,length,rank,data=None,space=None,types=None):
                    
        if data is None:
            self.data = np.zeros((length,rank,rank))
            self.rank = rank
            self.length = length
        else:
            self.data = data
            self.rank = data.shape[1]
            self.length = data.shape[0]
        
        if types is None:
            self.types = list(range(self.rank))
        else:
            assert len(types)==self.rank
            self.types
        
        if space is None:
            self.space = Space.Real
        else:
            self.space = space
            
    def __repr__(self):
        return '<MatrixArray rank:{:d} length:{:d}>'.format(self.rank,self.length)
    
    def itercolumn(self):
        for i,j in product(range(self.rank),range(self.rank)):
            if i<=j: #upper triangle condition
                type1 = self.types[i]
                type2 = self.types[j]
                yield (i,j),(type1,type2),self.data[:,i,j]
            
    def __setitem__(self,key,val):
        '''Column setter 
        
        Assumes all matrices are symmetric and enforces symmetry by
        setting both off diagonal elements. 
        '''
        index1,index2 = key
        self.data[:,index1,index2] = val
        if not (index1 == index2):
            self.data[:,index2,index1] = val
        
    def __getitem__(self,key):
        '''Column getter'''
        index1,index2 = key
        return self.data[:,index1,index2]
    
    def getByTypes(self,type1,type2):
        '''Column getter via supplied types
        
        .. warning::
        
            This getter should not be used in performance critical code
            as it has to look up the index of the semantic types.
        
        '''
        index1 = self.types.index(type1)
        index2 = self.types.index(type2)
        return self.data[:,index1,index2]
    
    def __truediv__(self,other):
        '''Scalar or elementwise division'''
        if type(other) is MatrixArray:
            assert self.space == other.space,MatrixArray.SpaceError
            data = self.data / other.data
        else:
            data = self.data / other
        return MatrixArray(length=self.length,rank=self.rank,data=data,space=self.space)
    
    def __itruediv__(self,other):
        '''Scalar or elementwise division'''
        if type(other) is MatrixArray:
            assert self.space == other.space,MatrixArray.SpaceError
            self.data /= other.data
        else:
            self.data /= other
        return self
    
    # def __rmul__(self,other):
    #     '''Scalar or elementwise multiplication'''
    #     return self.__mul__(other)
        
    def __mul__(self,other):
        '''Scalar or elementwise multiplication'''
        if type(other) is MatrixArray:
            assert self.space == other.space,MatrixArray.SpaceError
            data = self.data * other.data
        else:
            data = self.data * other
        return MatrixArray(length=self.length,rank=self.rank,data=data,space=self.space)
    
    def __imul__(self,other):
        '''Scalar or elementwise multiplication'''
        if type(other) is MatrixArray:
            assert self.space == other.space,MatrixArray.SpaceError
            self.data *= other.data
        else:
            self.data *= other
        return self
    
    # def __radd__(self,other):
    #     '''Scalar or elementwise addition'''
    #     return self.__add__(other)
            
    def __add__(self,other):
        if type(other) is MatrixArray:
            assert self.space == other.space,MatrixArray.SpaceError
            data = self.data + other.data
        else:
            data = self.data + other
        return MatrixArray(length=self.length,rank=self.rank,data=data,space=self.space)
    
    def __iadd__(self,other):
        if type(other) is MatrixArray:
            assert self.space == other.space,MatrixArray.SpaceError
            self.data += other.data
        else:
            self.data += other
        return self
            
    # def __rsub__(self,other):
    #     '''Scalar or elementwise subtraction'''
    #     return self.__sub__(other)
    
    def __sub__(self,other):
        if type(other) is MatrixArray:
            assert self.space == other.space,MatrixArray.SpaceError
            data = self.data - other.data
        else:
            data = self.data - other
        return MatrixArray(length=self.length,rank=self.rank,data=data,space=self.space)
    
    def __isub__(self,other):
        if type(other) is MatrixArray:
            assert self.space == other.space,MatrixArray.SpaceError
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
            
        data = np.linalg.inv(self.data)
            
        if inplace:
            self.data = data
            return self
        else:
            return MatrixArray(rank=self.rank,length=self.length,data=data,space=self.space)
        
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
            return self
        else:
            data = np.einsum('lij,ljk->lik', self.data, other.data)
            return MatrixArray(length=self.length,rank=self.rank,data=data,space=self.space)
        
    def __matmul__(self,other):
        assert self.space == other.space,MatrixArray.SpaceError
        return self.dot(other,inplace=False)
        
    def __imatmul__(self,other):
        assert self.space == other.space,MatrixArray.SpaceError
        return self.dot(other,inplace=True)
        
        