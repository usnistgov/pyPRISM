#!python
from __future__ import division,print_function
from pyPRISM.core.MatrixArray import MatrixArray
from pyPRISM.core.Density import Density
import unittest
import numpy as np

class Density_TestCase(unittest.TestCase):
    def test_create(self):
        '''Can we create a density object? '''
        types = ['A','B','C']
        d = Density(types)

        d['A'] = 0.5
        d['B'] = 0.25
        d['C'] = 0.1

    def test_createDensityMatrices(self):
        '''Can we construct the two necesssary density matrices?'''

        d = Density(['A','B'])
        
        d['A'] = rhoA = 0.45
        d['B'] = rhoB = 0.35
        
        siteDensityMatrix1 = np.zeros((1,2,2))
        siteDensityMatrix1[:,0,0] = [rhoA]
        siteDensityMatrix1[:,0,1] = [rhoA + rhoB]
        siteDensityMatrix1[:,1,0] = [rhoA + rhoB]
        siteDensityMatrix1[:,1,1] = [rhoB]
        
        pairDensityMatrix1 = np.zeros((1,2,2))
        pairDensityMatrix1[:,0,0] = [rhoA * rhoA]
        pairDensityMatrix1[:,0,1] = [rhoA * rhoB]
        pairDensityMatrix1[:,1,0] = [rhoB * rhoA]
        pairDensityMatrix1[:,1,1] = [rhoB * rhoB]
        
        np.testing.assert_array_almost_equal(d.site.data,siteDensityMatrix1)
        np.testing.assert_array_almost_equal(d.pair.data,pairDensityMatrix1)

if __name__ == '__main__':
    import unittest 
    suite = unittest.TestLoader().loadTestsFromTestCase(Density_TestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
