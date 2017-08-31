#!python
from typyPRISM.core.Space import Space
import string
from itertools import product
import numpy as np

class MatrixArray(object):
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

    Access to the MatrixArray is either by supplied types or numerical indices.
    If types are not supplied, captial letters starting from 'A' are used. 

    .. python::

        mArray = MatrixArray(length=1024,rank=2,types=['polymer','solvent'])
        
        mArray['polymer','solvent'] == mArray['solvent','polymer'] == mArray.get(0,1)

    
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
            self.types = list(string.ascii_uppercase[:rank])
        else:
            assert len(types)==self.rank
            self.types = types

        self.typeMap = {t:i for i,t in enumerate(self.types)}

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

        The key parameter should be a tuple of string types which
        '''
        type1,type2 = key 
        try:
            index1 = self.typeMap[type1]
            index2 = self.typeMap[type2]
        except KeyError:
            raise ValueError('Either {} or {} is not a type in this MatrixArray with types {}'.format(type1,type2,self.types))

        self.data[:,index1,index2] = val
        if not (index1 == index2):
            self.data[:,index2,index1] = val
        
    def __getitem__(self,key):
        '''Column getter'''
        type1,type2 = key 
        try:
            index1 = self.typeMap[type1]
            index2 = self.typeMap[type2]
        except KeyError:
            raise ValueError('Either {} or {} is not a type in this MatrixArray with types {}'.format(type1,type2,self.types))
        return self.data[:,index1,index2]
    
    def get(self,index1,index2):
        '''Column getter via indices

        This method should be slightly more efficient than the standard
        __getitem__. 
        '''
        assert index1<self.rank,'Supplied index out of range'
        assert index2<self.rank,'Supplied index out of range'
        return self.data[:,index1,index2]
    

    def __truediv__(self,other):
        '''Scalar or elementwise division'''
        if type(other) is MatrixArray:
            assert self.space == other.space,MatrixArray.SpaceError
            data = self.data / other.data
        else:
            data = self.data / other
        return MatrixArray(length=self.length,rank=self.rank,data=data,space=self.space)

    def __div__(self,other):
        return self.__truediv__(other)

    def __itruediv__(self,other):
        '''Scalar or elementwise division'''
        if type(other) is MatrixArray:
            assert self.space == other.space,MatrixArray.SpaceError
            self.data /= other.data
        else:
            self.data /= other
        return self

    def __idiv__(self,other):
        return self.__itruediv__(other)
    
    
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
        
        
