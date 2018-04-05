import unittest
from pyPRISM.core.PairTable import PairTable
from pyPRISM.core.MatrixArray import MatrixArray
from pyPRISM.core.Space import Space
import numpy as np

class PairTable_TestCase(unittest.TestCase):
    def test_get_set(self):
        '''Can we set and get values from the table?'''
        PT = PairTable(['A','B','C'],'density')
        PT['A','B'] = 0.4
        PT['A',['A','C']] = 0.25
        
        self.assertEqual(PT['A','B'],0.4)
        self.assertEqual(PT['B','A'],0.4)
        self.assertEqual(PT['A','A'],0.25)
        self.assertEqual(PT['A','C'],0.25)
        self.assertEqual(PT['C','A'],0.25)
        
    def test_check(self):
        '''Can we check to make sure the table is filled?'''
        PT = PairTable(['A','B','C'],'density')
        PT['A','B'] = 0.4
        PT['A',['A','C']] = 0.25
        self.assertRaises(ValueError,PT.check)
        
    def test_apply(self):
        '''Can we apply a function to the table?'''
        PT = PairTable(['A','B','C'],'density')
        PT['A','B'] = 0.4
        PT.setUnset(0.25)
        
        PT.apply(np.square)
        
        self.assertEqual(PT['A','B'],0.4*0.4)
        self.assertEqual(PT['B','A'],0.4*0.4)
        self.assertEqual(PT['A','A'],0.25*0.25)
        self.assertEqual(PT['A','C'],0.25*0.25)
        self.assertEqual(PT['C','A'],0.25*0.25)
        self.assertEqual(PT['C','C'],0.25*0.25)
        
        
        
        
    def test_setUnset(self):
        '''Can wet set all of the unset table values?'''
        PT = PairTable(['A','B','C'],'density')
        PT['A','B'] = 0.4
        PT.setUnset(0.25)
        
        self.assertEqual(PT['A','B'],0.4)
        self.assertEqual(PT['B','A'],0.4)
        self.assertEqual(PT['A','A'],0.25)
        self.assertEqual(PT['A','C'],0.25)
        self.assertEqual(PT['C','A'],0.25)
        self.assertEqual(PT['C','C'],0.25)
        
    def test_iter_full(self):
        '''Can we iterate over all of the table pairs?'''
        types = ['A','B','C']
        ntypes = len(types)
        PT = PairTable(types,'density')
        
        numericPairs = [
                         (0,0),(0,1),(0,2),
                         (1,0),(1,1),(1,2),
                         (2,0),(2,1),(2,2)
                       ]
        
        counter = 0
        for i,t,v in PT.iterpairs(full=True):
            if i in numericPairs:
                numericPairs.remove(i)
            counter+=1
            
        #did we visit all expected pairs?
        self.assertEqual(len(numericPairs),0)
        
        #sanity check, did we visit the correct number of pairs?
        self.assertEqual(counter,ntypes*ntypes)
        
    def test_iter_diagonal(self):
        '''Can we iterate over the upper triangle + diagonal?'''
        types = ['A','B','C']
        ntypes = len(types)
        PT = PairTable(types,'density')
        
        numericPairs = [
                         (0,0),(0,1),(0,2),
                               (1,1),(1,2),
                                     (2,2)
                       ]
        
        counter = 0
        for i,t,v in PT.iterpairs(diagonal=True):
            if i in numericPairs:
                numericPairs.remove(i)
            counter+=1
            
        #did we visit all expected pairs?
        self.assertEqual(len(numericPairs),0)
        
        #sanity check, did we visit the correct number of pairs?
        self.assertEqual(counter,ntypes*(ntypes+1)//2)
        
    def test_iter_triangle(self):
        '''Can we iterate over only the upper triangle?'''
        types = ['A','B','C']
        ntypes = len(types)
        PT = PairTable(types,'density')
        
        numericPairs = [
                         (0,1),(0,2),
                               (1,2),
                                    
                       ]
        
        counter = 0
        for i,t,v in PT.iterpairs(diagonal=False):
            if i in numericPairs:
                numericPairs.remove(i)
            counter+=1
            
        #did we visit all expected pairs?
        self.assertEqual(len(numericPairs),0)
        
        #sanity check, did we visit the correct number of pairs?
        self.assertEqual(counter,ntypes*(ntypes-1)//2)
    
    def test_MatrixArray_export(self):
        types = ['A','B','C']
        length = 1024
        rank = len(types)
        values1 = np.ones(length)
        values2 = np.ones(length)*5.0
        values3 = np.ones(length)*2.1234
        
        MA1 = MatrixArray(length=length,rank=rank,space=Space.Fourier)
        MA1['A','A'] = values2
        MA1['A','B'] = values1
        MA1['A','C'] = values1
        MA1['B','B'] = values3
        MA1['B','C'] = values3
        MA1['C','C'] = values3
        
        ntypes = len(types)
        PT = PairTable(types,'density')
        PT[['A'],['B','C']] = values1
        PT[['A'],['A']] = values2
        PT.setUnset(values3)
        MA2 = PT.exportToMatrixArray(space=Space.Fourier)
        
        np.testing.assert_array_almost_equal(MA1.data,MA2.data)
        self.assertEqual(MA1.space,MA2.space)
        
if __name__ == '__main__':
    import unittest 
    suite = unittest.TestLoader().loadTestsFromTestCase(PairTable_TestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
