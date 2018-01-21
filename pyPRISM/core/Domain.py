#!python
from __future__ import division,print_function
from pyPRISM.core.Space import Space
import numpy as np
from scipy.fftpack import dst

class Domain(object):
    r'''Define domain and transform between Real and Fourier space

    **Mathematical Definition**
        
        The continuous, 1-D, radially symmetric Fourier transform is written
        as follows:

        .. math::

            k\ \hat{f}(k) = 4 \pi \int r\ f(r) \sin(k\ r) dr

        We define the following discretizations

        .. math:: 

            r = (i+1)\Delta r

            k = (j+1)\Delta k

            \Delta k = \frac{\pi}{\Delta r (N + 1)}

        to yield

        .. math::

            \hat{F}_j = 4 \pi \Delta r \sum_{i=0}^{N-1} F_i \sin\left(\frac{\pi}{N+1} (i+1)(j+1)\right)

        with the following definitions:

        .. math::

            \hat{F}_j = (j+1)\ \Delta k\ \hat{f}((j+1)\Delta k) = k \hat{f}(k)

        .. math::

            F_i = (i+1)\Delta r\ f((i+1)\Delta r) = r f(r)

        The above equations describe a Real to Real, type-II discrete sine
        transform (DST). To tranform to and from Fourier space we will use the
        type-II and type-III DST's respectively. With Scipy's interface to
        fftpack, the following functional coeffcients are

        .. math::

            C^{DSTII} = 2 \pi r \Delta r

        .. math::

            C^{DSTIII} = \frac{k \Delta k}{4 \pi^2}
    
    
    **Description**

        Domain describes the discretization of Real and Fourier space
        and also sets up the functions and coefficients for transforming
        data between them.
    
    '''
    def __init__(self,length,dr=None,dk=None):
        r'''Constructor

        Arguments
        ---------
        length: int
            Number of gridpoints in Real and Fourier space grid

        dr,dk: float
            Grid spacing in Real space or Fourier space. Only one can be
            specified as it fixes the other.

        '''
        self._length = length
        
        if (dr is None) and (dk is None):
            raise ValueError('Real or Fourier grid spacing must be specified')
            
        elif (dr is not None) and (dk is not None):
            raise ValueError('Cannot specify **both** Real and Fourier grid spacings independently.')
            
        elif dr is not None:
            self.dr = dr #dk is set in property setter
            
        elif dk is not None:
            self.dk = dk #dr is set in property setter
            
            
        self.build_grid() #build grid should have been called already but we'll be safe
    
    def build_grid(self):
        '''Construct the Real and Fourier Space grids and transform coefficients'''
        self.r = np.arange(self._dr,self._dr*(self._length+1),self._dr)
        self.k = np.arange(self.dk,self.dk*(self._length+1),self.dk)
        self.DST_II_coeffs = 2.0*np.pi *self.r*self._dr 
        self.DST_III_coeffs = self.k * self.dk/(4.0*np.pi*np.pi)
        self.long_r = self.r.reshape((-1,1,1))
    
    @property
    def dr(self):
        '''Real grid spacing'''
        return self._dr
    @dr.setter
    def dr(self,value):
        self._dr = value
        self._dk = np.pi/(self._dr*self._length)
        self.build_grid()#need to re-build grid since spacing has changed
    
    @property
    def dk(self):
        '''Fourier grid spacing'''
        return self._dk
    @dk.setter
    def dk(self,value):
        self._dk = value
        self._dr = np.pi/(self._dk*self._length)
        self.build_grid()#need to re-build grid since spacing has changed
        
    @property
    def length(self):
        '''Number of points in grid'''
        return self._length
    @length.setter
    def length(self,value):
        self._length = value
        self.build_grid()#need to re-build grid since length has changed
        
    def __repr__(self):
        return '<Domain length:{} dr/rmax:{:4.3f}/{:3.1f} dk/kmax:{:4.3f}/{:3.1f}>'.format(self.length,self.dr,self.r[-1],self.dk,self.k[-1])
    
    def to_fourier(self,array):
        r''' Discrete Sine Transform of a numpy array 
        
        Arguments
        ---------
        array: float ndarray
            Real-space data to be transformed
            
        Returns
        -------
        array: float ndarray
            data transformed to fourier space


        Peforms a Real-to-Real Discrete Sine Transform  of type II 
        on a numpy array of non-complex values. For radial data that is 
        symmetric in :math:`\phi` and :math`\theta`, this is a correct transform
        to go from Real-space to Fourier-space. 
        
        
        '''
        return dst(self.DST_II_coeffs*array,type=2)/self.k
    
    def to_real(self,array):
        ''' Discrete Sine Transform of a numpy array 
        
        Arguments
        ---------
        array: float ndarray
            Fourier-space data to be transformed
            
        Returns
        -------
        array: float ndarray
            data transformed to Real space

        Peforms a Real-to-Real Discrete Sine Transform  of type III
        on a numpy array of non-complex values. For radial data that is 
        symmetric in :math:`\phi` and :math`\theta`, this is a correct transform
        to go from Real-space to Fourier-space. 
        
        '''
        return dst(self.DST_III_coeffs*array,type=3)/self.r
    
    def MatrixArray_to_fourier(self,marray):
        ''' Transform all curves of a MatrixArray to Fourier space in-place

        Arguments
        ---------
        marray: :class:`pyPRISM.core.MatrixArray.MatrixArray`
            MatrixArray to be transformed

        Raises
        ------
        *ValueError*:
            If the supplied MatrixArray is already in Real-space
        '''
        if marray.space == Space.Fourier:
            raise ValueError('MatrixArray is marked as already in Fourier space')
            
        for (i,j),(t1,t2),curve in marray.itercurve():
            marray[t1,t2] = self.to_fourier(curve)
        
        marray.space = Space.Fourier
            
    def MatrixArray_to_real(self,marray):
        ''' Transform all curves of a MatrixArray to Real space in-place 

        Arguments
        ---------
        marray: :class:`pyPRISM.core.MatrixArray.MatrixArray`
            MatrixArray to be transformed

        Raises
        ------
        ValueError:
            If the supplied MatrixArray is already in Real-space
        '''
        if marray.space == Space.Real:
            raise ValueError('MatrixArray is marked as already in Real space')
            
        for (i,j),(t1,t2),curve in marray.itercurve():
            marray[t1,t2] = self.to_real(curve)
            
        marray.space = Space.Real
            
