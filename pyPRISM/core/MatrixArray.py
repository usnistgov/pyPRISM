#!python
from pyPRISM.core.Space import Space
import string
from itertools import product
import numpy as np
from scipy.signal import fftconvolve
from scipy.ndimage.filters import convolve

class MatrixArray(object):
    '''A container for creating and interacting with arrays of matrices
    
    **Description**

        The primary data structure of MatrixArray is simply a 3D Numpy array 
        with the first dimension accessing each individual matrix in the array
        and the last two dimenions corresponding to the vertical and horizontal 
        index of each matrix element.
        
        The terminology *Curve* is used to refer to the set of values from
        all matrices in the array at a given matrix index pair. In Numpy slicing 
        parlance::
        
            curve_11 = numpy_array[:,1,1]
            curve_12 = numpy_array[:,1,2]

        Access to the MatrixArray is either by supplied types or numerical indices.
        If types are not supplied, captial letters starting from 'A' are used. 

        See the example below and the `pyPRISM Internals` section of the
        :ref:`tutorial` for more information.

    Example
    -------
    .. code-block:: python

        mArray = MatrixArray(length=1024,rank=2,types=['polymer','solvent'])
        
        mArray['polymer','solvent'] == mArray['solvent','polymer'] == mArray.get(0,1)

    
    '''
    
    SpaceError = "Attempting MatrixArray math in non-matching spaces"
    
    def __init__(self,length,rank,data=None,space=Space.Real,types=None):
        '''Constructor

        Arguments
        ----------
        length: int
            Number of matrices in array. For PRISM theory, this corresponds to
            the number of grid points in real- and Fourier-space i.e.
            Domain.size.

        rank: int
            Number of rows/cols of each (square) matrix. For PRISM theory, this
            also equal to the number of site types.
            
        data: np.ndarray, size (length,rank,rank)
            Interface for specifying the MatrixArray data directly. If not
            given, all values in all matrices will be set to zero. 
            
        space: pyPRISM.core.Space.Space
            Enumerated value tracking whether the array represents real or
            Fourier spaced data. As we will be transferring arrays to and from
            these spaces, it's important for safety that we track this.

        types: list, *optional*
            List of semantic types that are be used to reference data. These
            types will be output by the itercurve method as well. If not
            supplied, uppercase letters will be used.

        '''
                    
        if data is None:
            self.data = np.zeros((length,rank,rank))
            self.rank = rank
            self.length = length
        else:
            assert len(data.shape)==3,'Data passed to MatrixArray must be 3-D'
            assert data.shape[1]==data.shape[2],'Last two dimensions of MatrixArray data must be same size'
            self.data = data
            self.rank = data.shape[1]
            self.length = data.shape[0]
        
        if types is None:
            self.types = list(string.ascii_uppercase[:self.rank])
        else:
            assert len(types)==self.rank
            self.types = types

        self.typeMap = {t:i for i,t in enumerate(self.types)}
        self.space = space

    def __repr__(self):
        return '<MatrixArray rank:{:d} length:{:d}>'.format(self.rank,self.length)
    
    def get_copy(self):
        '''Return an independent copy of this MatrixArray'''
        return MatrixArray(length=self.length,rank=self.rank,data=np.copy(self.data),space=self.space,types=self.types)
    
    def itercurve(self):
        '''Iterate over the curves in this MatrixArray

        Yields
        ------
        (i,j): 2-tuple of integers
            numerical index to the underlying data numpy array

        (t1,t2): 2-tuple of string types
            string index to the underlying data numpy array

        curve: np.ndarray, size (self.length)
            1-D array representing a curve within the MatrixArray
        '''
        for i,j in product(range(self.rank),range(self.rank)):
            if i<=j: #upper triangle condition
                type1 = self.types[i]
                type2 = self.types[j]
                yield (i,j),(type1,type2),self.data[:,i,j]
            
    def __setitem__(self,key,val):
        '''Curve setter 

        Arguments
        ---------
        key: tuple of types
            Type pair used to identify curve pair

        val: np.ndarray
            Values of curve


        Assumes all matrices are symmetric and enforces symmetry by
        setting the off-diagonal elements to be equal.

        '''
        type1,type2 = key 

        try:
            index1 = self.typeMap[type1]
        except KeyError:
            raise ValueError('This MatrixArray has types: {}. You requested type: \'{}\''.format(self.types,type1))

        try:
            index2 = self.typeMap[type2]
        except KeyError:
            raise ValueError('This MatrixArray has types: {}. You requested type: \'{}\''.format(self.types,type2))

        self.data[:,index1,index2] = val
        if not (index1 == index2):
            self.data[:,index2,index1] = val
        
    def __getitem__(self,key):
        '''Curve getter

        Arguments
        ---------
        key: tuple of types
            Type pair used to identify curve pair

        val: np.ndarray
            Values of curve
        '''

        type1,type2 = key 

        try:
            index1 = self.typeMap[type1]
        except KeyError:
            raise ValueError('This MatrixArray has types: {}. You requested type: \'{}\''.format(self.types,type1))

        try:
            index2 = self.typeMap[type2]
        except KeyError:
            raise ValueError('This MatrixArray has types: {}. You requested type: \'{}\''.format(self.types,type2))

        return self.data[:,index1,index2]
    
    def get(self,index1,index2):
        '''Curve getter via indices

        This method should be slightly more efficient than the standard
        __getitem__. 
        '''
        assert index1<self.rank,'Supplied index out of range'
        assert index2<self.rank,'Supplied index out of range'
        return self.data[:,index1,index2]

    def getMatrix(self,matrix_index):
        '''Matrix getter via indices'''
        return self.data[matrix_index,:,:]

    def setMatrix(self,matrix_index,value):
        '''Matrix setter via indices'''
        self.data[matrix_index,:,:] = value
    

    def __truediv__(self,other):
        '''Scalar or elementwise division'''
        if isinstance(other,MatrixArray):
            assert (self.space == other.space) or (Space.NonSpatial in (self.space,other.space)),MatrixArray.SpaceError
            data = self.data / other.data
        else:
            data = self.data / other
        return MatrixArray(length=self.length,rank=self.rank,data=data,space=self.space,types=self.types)

    def __div__(self,other):
        return self.__truediv__(other)

    def __itruediv__(self,other):
        '''Scalar or elementwise division'''
        if isinstance(other,MatrixArray):
            assert (self.space == other.space) or (Space.NonSpatial in (self.space,other.space)),MatrixArray.SpaceError
            self.data /= other.data
        else:
            self.data /= other
        return self

    def __idiv__(self,other):
        return self.__itruediv__(other)
    
    
    def __mul__(self,other):
        '''Scalar or elementwise multiplication'''
        if isinstance(other,MatrixArray):
            assert (self.space == other.space) or (Space.NonSpatial in (self.space,other.space)),MatrixArray.SpaceError
            data = self.data * other.data
        else:
            data = self.data * other
        return MatrixArray(length=self.length,rank=self.rank,data=data,space=self.space,types=self.types)
    
    def __imul__(self,other):
        '''Scalar or elementwise multiplication'''
        if isinstance(other,MatrixArray):
            assert (self.space == other.space) or (Space.NonSpatial in (self.space,other.space)),MatrixArray.SpaceError
            self.data *= other.data
        else:
            self.data *= other
        return self
    
    def __add__(self,other):
        if isinstance(other,MatrixArray):
            assert (self.space == other.space) or (Space.NonSpatial in (self.space,other.space)),MatrixArray.SpaceError
            data = self.data + other.data
        else:
            data = self.data + other
        return MatrixArray(length=self.length,rank=self.rank,data=data,space=self.space,types=self.types)
    
    def __iadd__(self,other):
        if isinstance(other,MatrixArray):
            assert (self.space == other.space) or (Space.NonSpatial in (self.space,other.space)),MatrixArray.SpaceError
            self.data += other.data
        else:
            self.data += other
        return self
            
    def __sub__(self,other):
        if isinstance(other,MatrixArray):
            assert (self.space == other.space) or (Space.NonSpatial in (self.space,other.space)),MatrixArray.SpaceError
            data = self.data - other.data
        else:
            data = self.data - other
        return MatrixArray(length=self.length,rank=self.rank,data=data,space=self.space,types=self.types)
    
    def __isub__(self,other):
        if isinstance(other,MatrixArray):
            assert (self.space == other.space) or (Space.NonSpatial in (self.space,other.space)),MatrixArray.SpaceError
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
            return MatrixArray(rank=self.rank,length=self.length,data=data,space=self.space,types=self.types)
        
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
        if isinstance(other,MatrixArray):
            assert (self.space == other.space) or (Space.NonSpatial in (self.space,other.space)),MatrixArray.SpaceError
        if inplace:
            self.data = np.einsum('lij,ljk->lik', self.data, other.data)
            return self
        else:
            data = np.einsum('lij,ljk->lik', self.data, other.data)
            return MatrixArray(length=self.length,rank=self.rank,data=data,space=self.space,types=self.types)
        
    def MatrixConvolve(self,other,dr,inplace=False):
        ''' Matrix multiplication-like convolution for to MatrixArrays 
        
        Parameters
        ----------
        other: object, MatrixArray
            Must be an object of MatrixArray type of the same length
            and dimension
            
        inplace: bool
            If False, a new MatrixArray is returned, otherwise just
            update the internal data.
        
        '''
        if isinstance(other,MatrixArray):
            assert (self.space == other.space) or (Space.NonSpatial in (self.space,other.space)),MatrixArray.SpaceError
        
        rows_self = self.data.shape[1]
        cols_self = self.data.shape[2]
        rows_other = other.data.shape[1]
        cols_other = other.data.shape[2]

        # sanity check
        assert cols_self == rows_other
        
        result = np.zeros_like(self.data)
        for i in range(rows_self):
          for j in range(cols_other):
            for k in range(cols_self):
              # temp = fftconvolve(self.data[:,i,k],other.data[:,k,j],mode='same')
              temp = fftconvolve(self.data[:,i,k],other.data[:,k,j],mode='full')[:self.data.shape[0]]
              # temp = convolve(self.data[:,i,k],other.data[:,k,j],mode='constant')
              # temp = np.convolve(self.data[:,i,k],other.data[:,k,j],mode='full')[:self.data.shape[0]]
              result[:,i,j] += (temp*dr).flatten()
        
        if inplace:
            self.data = result 
            return self
        else:
            data = result 
            return MatrixArray(length=self.length,rank=self.rank,data=data,space=self.space,types=self.types)
    
    def __matmul__(self,other):
        assert (self.space == other.space) or (Space.NonSpatial in (self.space,other.space)),MatrixArray.SpaceError
        return self.dot(other,inplace=False)
        
    def __imatmul__(self,other):
        assert (self.space == other.space) or (Space.NonSpatial in (self.space,other.space)),MatrixArray.SpaceError
        return self.dot(other,inplace=True)
        
        
