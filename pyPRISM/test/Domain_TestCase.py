#!python
from __future__ import division,print_function
from pyPRISM.core.MatrixArray import MatrixArray
from pyPRISM.core.Domain import Domain
import unittest
import numpy as np

class Domain_TestCase(unittest.TestCase):
    def test_MatrixArray_loop(self):
        '''Can we transform an entire MatrixArray?'''
        length = 1024
        rank = 3
        dr = 0.1
        d = Domain(length=length,dr=dr)
        
        array1 = np.sin(np.arange(0,10*np.pi,0.01))[:length]
        array2 = 5*np.sin(np.arange(0,10*np.pi,0.01))[:length]
        array3 = np.cos(np.arange(0,10*np.pi,0.01))[:length]
        array4 = np.cos(np.arange(0,10*np.pi,0.01))[:length] + np.sin(np.arange(0,10*np.pi,0.01))[:length]
        
        MA = MatrixArray(length=length,rank=rank)
        MA['A','A'] = array1
        MA['B','B'] = array2
        MA['B','C'] = array3
        MA['C','C'] = array4
        
        d.MatrixArray_to_fourier(MA)
        np.testing.assert_array_almost_equal(MA['A','A'],d.to_fourier(array1))
        np.testing.assert_array_almost_equal(MA['B','B'],d.to_fourier(array2))
        np.testing.assert_array_almost_equal(MA['B','C'],d.to_fourier(array3))
        np.testing.assert_array_almost_equal(MA['C','B'],d.to_fourier(array3))
        np.testing.assert_array_almost_equal(MA['C','C'],d.to_fourier(array4))
        
        # This should recover the original values of the MatrixArray
        d.MatrixArray_to_real(MA)
        np.testing.assert_array_almost_equal(MA['A','A'],array1)
        np.testing.assert_array_almost_equal(MA['B','B'],array2)
        np.testing.assert_array_almost_equal(MA['B','C'],array3)
        np.testing.assert_array_almost_equal(MA['C','B'],array3)
        np.testing.assert_array_almost_equal(MA['C','C'],array4)
        
    def test_array_loop(self):
        '''Can we go to Fourier space and back again?'''
        d = Domain(length=1024,dr=0.1)
        
        real_space_data1 = np.sin(np.arange(0,10*np.pi,0.01))[:1024]
        
        fourier_space_data = d.to_fourier(real_space_data1)
        
        real_space_data2 = d.to_real(fourier_space_data)
        
        # If the DST coefficients are correct, we should get back (within numerical
        # precision) the same array we started with.
        np.testing.assert_array_almost_equal(real_space_data1,real_space_data2)

if __name__ == '__main__':
    import unittest 
    suite = unittest.TestLoader().loadTestsFromTestCase(Domain_TestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
