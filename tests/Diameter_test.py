#!python
from __future__ import division,print_function
from pyPRISM.core.MatrixArray import MatrixArray
from pyPRISM.core.Diameter import Diameter
import unittest
import numpy as np

class Diameter_TestCase(unittest.TestCase):
    def test_create(self):
        '''Can we create a diameter object? '''
        types = ['A','B','C']
        d = Diameter(types)

        d['A'] = 0.5
        d['B'] = 0.25
        d['C'] = 0.1

        np.testing.assert_almost_equal(d['A'],0.5)
        np.testing.assert_almost_equal(d['B'],0.25)
        np.testing.assert_almost_equal(d['C'],0.1)


    def test_sigma(self):
        '''Can we create the sigma matrix? '''
        types = ['A','B','C']
        d = Diameter(types)

        d['A'] = 0.5
        d['B'] = 0.25
        d['C'] = 0.1

        SigmaMatrix1 = np.zeros((3,3))
        for (i,j),t,v in d.sigma:
            SigmaMatrix1[i,j] = v

        SigmaMatrix2 = np.zeros((3,3))
        SigmaMatrix2[0,0] = (d['A']+d['A'])/2.0
        SigmaMatrix2[0,1] = (d['A']+d['B'])/2.0
        SigmaMatrix2[0,2] = (d['A']+d['C'])/2.0
        SigmaMatrix2[1,0] = (d['B']+d['A'])/2.0
        SigmaMatrix2[1,1] = (d['B']+d['B'])/2.0
        SigmaMatrix2[1,2] = (d['B']+d['C'])/2.0
        SigmaMatrix2[2,0] = (d['C']+d['A'])/2.0
        SigmaMatrix2[2,1] = (d['C']+d['B'])/2.0
        SigmaMatrix2[2,2] = (d['C']+d['C'])/2.0

        np.testing.assert_array_almost_equal(SigmaMatrix1,SigmaMatrix2)



if __name__ == '__main__':
    import unittest 
    suite = unittest.TestLoader().loadTestsFromTestCase(Diameter_TestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
