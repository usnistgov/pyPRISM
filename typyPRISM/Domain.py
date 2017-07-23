
import numpy as np
from scipy.fftpack import dst

class Domain:
    ''' Define and transform between real and Fourier space
    
    Domain describes the discretization of real and Fourier space
    and also sets up the functions and coefficients for transforming
    data between them.
    
    Attributes
    ----------
    length: int
        Number of gridpoints in real and Fourier space grid
        
    dr,dk: float
        Grid spacing in real and Fourier space
    
    r,k: float ndarray
        Numpy arrays of grid locations in real and Fourier space
    
    DST_II_coeffs,DST_III_coeffs: float
        Coefficients needed for Discrete Sine Transforms. Note that these
        values are specific to each implementation of the DST and were 
        derived for (Scipy's interface to) FFTPACK. 
    '''
    __slots__ = ('length',
                 'r','dr',
                 'k','dk',
                 'DST_II_coeffs','DST_III_coeffs')
    def __init__(self,length,dr):
        self.length = length
        
        self.dr = dr
        self.r = np.arange(dr,dr*(length+1),dr)
        
        self.dk = np.pi/(dr*length)
        self.k = np.arange(self.dk,self.dk*(length+1),self.dk)
        
        self.DST_II_coeffs = 2.0*np.pi*self.r*dr 
        self.DST_III_coeffs = self.k * self.dk/(4.0*np.pi*np.pi)
        
    def __repr__(self):
        return '<Domain length:{} dr/rmax:{:4.3f}/{:3.1f} dk/kmax:{:4.3f}/{:3.1f}>'.format(self.length,self.dr,self.r[-1],self.dk,self.k[-1])
    
    def to_fourier(self,array):
        ''' Discrete Sine Transform of a numpy array 
        
        Peforms a real-to-real Discrete Sine Transform  of type II 
        on a numpy array of non-complex values. For radial data that is 
        symmetric in \phi and \theta, this is **a** correct transform
        to go from real-space to Fourier-space. 
        
        Parameters
        ----------
        array: float ndarray
            real-space data to be transformed
            
        Returns
        -------
        array: float ndarray
            data transformed to fourier space
        
        '''
        return dst(self.DST_II_coeffs*array,type=2)/self.k
    
    def to_real(self,array):
        ''' Discrete Sine Transform of a numpy array 
        
        Peforms a real-to-real Discrete Sine Transform  of type III 
        on a numpy array of non-complex values. For radial data that is 
        symmetric in \phi and \theta, this is **a** correct transform
        to go from Fourier-space to real space.
        
        Parameters
        ----------
        array: float ndarray
            Fourier-space data to be transformed
            
        Returns
        -------
        array: float ndarray
            data transformed to real space
        
        '''
        return dst(self.DST_III_coeffs*array,type=3)/self.r
    
    def MatrixArray_to_fourier(self,marray):
        ''' Transform all columns of a MatrixArray to Fourier space in-place'''
        for (i,j),column in marray.itercolumn():
            marray[i,j] = self.to_fourier(column)
            
    def MatrixArray_to_real(self,marray):
        ''' Transform all columns of a MatrixArray to real space in-place '''
        for (i,j),column in marray.itercolumn():
            marray[i,j] = self.to_real(column)
            