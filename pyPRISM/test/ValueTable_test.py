import unittest
from pyPRISM.core.ValueTable import ValueTable
import numpy as np

class ValueTable_TestCase(unittest.TestCase):
    def test_get_set(self):
        '''Can we set and get values from the table?'''
        VT = ValueTable(['A','B','C'],'density')
        VT['A'] = 0.4
        VT[['B','C']] = 0.25
        
        self.assertEqual(VT['A'],0.4)
        self.assertEqual(VT['B'],0.25)
        self.assertEqual(VT['C'],0.25)
        
    def test_check(self):
        '''Can we check to make sure the table is filled?'''
        VT = ValueTable(['A','B','C'],'density')
        VT[['A','B']] = 0.4
        self.assertRaises(ValueError,VT.check)
        
        
    def test_setUnset(self):
        '''Can wet set all of the unset table values?'''
        VT = ValueTable(['A','B','C'],'density')
        VT['A'] = 0.4
        VT.setUnset(0.25)
        self.assertEqual(VT['A'],0.4)
        self.assertEqual(VT['B'],0.25)
        self.assertEqual(VT['C'],0.25)
        
        
    def test_iter(self):
        '''Can we iterate over the table?'''
        types = ['A','B','C']
        ntypes = len(types)
        VT = ValueTable(types,'density')
        
        alphaTypes = ['A','B','C']
        
        counter = 0
        for i,t,v in VT:
            if t in alphaTypes:
                alphaTypes.remove(t)
            counter+=1
            
        #did we visit all expected pairs?
        self.assertEqual(len(alphaTypes),0)
        
        #sanity check, did we visit the correct number of pairs?
        self.assertEqual(counter,ntypes)
        
        
        
        
        
