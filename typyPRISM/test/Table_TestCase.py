import unittest
from typyPRISM.PairTable import PairTable
import numpy as np

class PairTable_TestCase(unittest.TestCase):
    def test_get_set(self):
        '''Can wet set and get values from the table?'''
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
        
        
    def test_pair_setUnset(self):
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
        
        
        
        