#!python
from pyPRISM.core.MatrixArray import MatrixArray
import numpy as np
import unittest

class MatrixArray_TestCase(unittest.TestCase): 
    def test_assign(self):
        '''Can we create and assign values?'''
        length = 100
        rank = 8
        MA = MatrixArray(length=length,rank=rank)
        
        # Make sure the array starts as all zeros
        array = np.zeros((length,rank,rank))
        np.testing.assert_array_almost_equal(MA.data,array)
        
        #  Test assignment (especially off diagonal)
        array = np.zeros((length,rank,rank))
        MA['B','B'] = np.ones(length)
        MA['B','C'] = np.ones(length)*3.0
        array[:,1,1] = np.ones(length)
        array[:,1,2] = np.ones(length)*3.0
        array[:,2,1] = np.ones(length)*3.0
        np.testing.assert_array_almost_equal(MA.data,array)
        
    def test_div(self):
        '''Can we truediv and itruediv?'''
        
        length = 100
        rank = 3
        (MA1,MA2),(array1,array2) = self.set_up_test_arrays(length,rank)
        
        MA2['A','C'] = np.ones(length)*2.0
        MA2['A','B'] = np.ones(length)*3.0
        MA2['B','C'] = np.ones(length)*5.0
        MA2['A','A'] += 1.0
        
        array2[:,0,2] = array2[:,2,0] = np.ones(length)*2.0
        array2[:,0,1] = array2[:,1,0] = np.ones(length)*3.0
        array2[:,1,2] = array2[:,2,1] = np.ones(length)*5.0
        array2[:,0,0] += 1.0
        
        ## Test Add
        MA3 = MA1 / MA2
        array3 = array1 / array2
        MA3 = MA3 / 542.345
        array3 = array3 / 542.345
        np.testing.assert_array_almost_equal(MA1.data,array1)
        np.testing.assert_array_almost_equal(MA2.data,array2)
        np.testing.assert_array_almost_equal(MA3.data,array3)
        
        ## Test iAdd
        MA3 /= MA2
        array3 /= array2
        MA3 /= 324
        array3 /= 324
        np.testing.assert_array_almost_equal(MA1.data,array1)
        np.testing.assert_array_almost_equal(MA2.data,array2)
        np.testing.assert_array_almost_equal(MA3.data,array3)
        
    def set_up_test_arrays(self,length=100,rank=3):
        ''' Helper for set up arrays to test math'''
        MA1 = MatrixArray(length=length,rank=rank)
        MA1['A','A'] = np.ones(length)*2.0
        MA1['B','B'] = np.ones(length)
        MA1['C','C'] = np.ones(length)*3.0
        MA1['B','C'] = np.ones(length)*3.0
        
        MA2 = MatrixArray(length=length,rank=rank)
        MA2['A','A'] = np.arange(length)
        MA2['B','B'] = np.ones(length)*2.0
        MA2['C','C'] = np.ones(length)*-3.0
        
        array1 = np.zeros((length,rank,rank))
        array1[:,0,0] = np.ones(length)*2.0
        array1[:,1,1] = np.ones(length)
        array1[:,2,2] = np.ones(length)*3.0
        array1[:,1,2] = np.ones(length)*3.0
        array1[:,2,1] = np.ones(length)*3.0
        
        array2 = np.zeros((length,rank,rank))
        array2[:,0,0] = np.arange(length)
        array2[:,1,1] = np.ones(length)*2.0
        array2[:,2,2] = np.ones(length)*-3.0
        return (MA1,MA2),(array1,array2)
        
    def test_add(self):
        '''Can we add and iadd?'''
        
        length = 100
        rank = 3
        (MA1,MA2),(array1,array2) = self.set_up_test_arrays(length,rank)
        
        ## Test Add
        MA3 = MA1 + MA2
        array3 = array1 + array2
        MA3 = MA3 + 2.53
        array3 = array3 + 2.53
        np.testing.assert_array_almost_equal(MA1.data,array1)
        np.testing.assert_array_almost_equal(MA2.data,array2)
        np.testing.assert_array_almost_equal(MA3.data,array3)
        
        ## Test iAdd
        MA3 += MA2
        MA3 += 435.43
        array3 += array2
        array3 += 435.43
        np.testing.assert_array_almost_equal(MA1.data,array1)
        np.testing.assert_array_almost_equal(MA2.data,array2)
        np.testing.assert_array_almost_equal(MA3.data,array3)
        
    def test_sub(self):
        '''Can we sub and isub?'''
        
        length = 100
        rank = 3
        (MA1,MA2),(array1,array2) = self.set_up_test_arrays(length,rank)
        
        ## Test Add
        MA3 = MA1 - MA2
        array3 = array1 - array2
        MA3 = MA3 - 852.32
        array3 = array3 - 852.32
        np.testing.assert_array_almost_equal(MA1.data,array1)
        np.testing.assert_array_almost_equal(MA2.data,array2)
        np.testing.assert_array_almost_equal(MA3.data,array3)
        
        ## Test iAdd
        MA3 -= MA2
        array3 -= array2
        MA3 -= 2
        array3 -= 2
        np.testing.assert_array_almost_equal(MA1.data,array1)
        np.testing.assert_array_almost_equal(MA2.data,array2)
        np.testing.assert_array_almost_equal(MA3.data,array3)
        
    def test_mul(self):
        '''Can we mul and imul?'''
        
        length = 100
        rank = 3
        (MA1,MA2),(array1,array2) = self.set_up_test_arrays(length,rank)
        
        ## Test Add
        MA3 = MA1 * MA2
        array3 = array1 * array2
        MA3 = MA3 * 542.345
        array3 = array3 * 542.345
        np.testing.assert_array_almost_equal(MA1.data,array1)
        np.testing.assert_array_almost_equal(MA2.data,array2)
        np.testing.assert_array_almost_equal(MA3.data,array3)
        
        ## Test iAdd
        MA3 *= MA2
        array3 *= array2
        MA3 *= 324
        array3 *= 324
        np.testing.assert_array_almost_equal(MA1.data,array1)
        np.testing.assert_array_almost_equal(MA2.data,array2)
        np.testing.assert_array_almost_equal(MA3.data,array3)
        
    def test_invert(self):
        '''Can we matrix invert?'''
        
        length = 100
        rank = 3
        (MA1,_),(array1,_) = self.set_up_test_arrays(length,rank)
        
        MA2 = MA1.invert(inplace=False)
        
        array2 = np.empty_like(array1)
        for i in range(length):
            array2[i] = np.linalg.inv(array1[i])
        
        np.testing.assert_array_almost_equal(MA1.data,array1)
        np.testing.assert_array_almost_equal(MA2.data,array2)
        
        MA1.invert(inplace=True)
        np.testing.assert_array_almost_equal(MA1.data,MA2.data)
        
    def test_dot(self):
        '''Can we matrix multiply?'''
        
        length = 100
        rank = 3
        (MA1,MA2),(array1,array2) = self.set_up_test_arrays(length,rank)
        
        MA3 = MA1.dot(MA2,inplace=False)
        
        array3 = np.empty_like(array1)
        for i in range(length):
            array3[i] = np.dot(array1[i],array2[i])
        
        np.testing.assert_array_almost_equal(MA1.data,array1)
        np.testing.assert_array_almost_equal(MA2.data,array2)
        np.testing.assert_array_almost_equal(MA3.data,array3)
        
        MA1.dot(MA2,inplace=True)
        np.testing.assert_array_almost_equal(MA1.data,MA3.data)
        
    def test_itercurve(self):
        ''' Can we iterate over the curves?'''
        length = 100
        rank = 5
        (MA1,_),(array1,_) = self.set_up_test_arrays(length,rank)
        
        ncols = 0
        for (i,j),(t1,t2),col in MA1.itercurve():
            # with self.subTest(i=i,j=j):
            #     np.testing.assert_array_almost_equal(col,array1[:,i,j])
            np.testing.assert_array_almost_equal(col,array1[:,i,j])
            ncols+=1
        self.assertEqual(ncols,rank*(rank+1)//2)
                
    def test_itercurve_assign(self):
        ''' Can we assign as we iterate over the curves?'''
        length = 100
        rank = 4
        (MA1,_),(array1,_) = self.set_up_test_arrays(length,rank)
        
        ncols = 0
        for (i,j),(t1,t2),col in MA1.itercurve():
            MA1[t1,t2] = np.ones(length)*i + j/2.0
            array1[:,i,j] = np.ones(length)*i + j/2.0
            array1[:,j,i] = np.ones(length)*i + j/2.0
            ncols += 1 
            
        np.testing.assert_array_almost_equal(MA1.data,array1)
        self.assertEqual(ncols,rank*(rank+1)//2)
            
    def test_get(self):
        ''' Can we access the data indices?'''
        length = 100
        rank = 3
        types = ['A','B','C']
        (MA1,_),(array1,_) = self.set_up_test_arrays(length,rank)
        
        MA1.types = types
        
        np.testing.assert_array_almost_equal(MA1['A','A'],MA1.get(0,0))
        np.testing.assert_array_almost_equal(MA1['A','B'],MA1.get(0,1))
        np.testing.assert_array_almost_equal(MA1['A','C'],MA1.get(0,2))
        np.testing.assert_array_almost_equal(MA1['B','A'],MA1.get(1,0))
        np.testing.assert_array_almost_equal(MA1['B','B'],MA1.get(1,1))
        np.testing.assert_array_almost_equal(MA1['B','C'],MA1.get(1,2))
        np.testing.assert_array_almost_equal(MA1['C','A'],MA1.get(2,0))
        np.testing.assert_array_almost_equal(MA1['C','B'],MA1.get(2,1))
        np.testing.assert_array_almost_equal(MA1['C','C'],MA1.get(2,2))
        
            
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MatrixArray_TestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
