#!python
from __future__ import division,print_function
import typyPRISM
import unittest
import numpy as np

class System_TestCase(unittest.TestCase):
    def test_create(self):
        '''Can we create a system?'''
        types = ['A','B','C']
        sys = typyPRISM.System(types)
    def test_check(self):
        '''Can we validate a system object?'''
        types = ['A','B','C']
        sys = typyPRISM.System(types)
        self.assertRaises(ValueError,sys.check)
        
        # These values make no sense but their sufficient
        # for this 'check'
        sys.domain = 'dummy'
        sys.density.setUnset(1.0)
        sys.potential.setUnset(1.0)
        sys.closure.setUnset(1.0)
        sys.omega.setUnset(1.0)
        
        #test should fail if this raises
        try:
            sys.check()
        except ValueError:
            self.fail('Check failed when it should have passed...')
    def test_createPRISM(self):
        '''Can we construct a simple but fully specified PRISM problem?'''
        
        sys = typyPRISM.System(['A','B'])
        
        sys.domain = typyPRISM.Domain(dr=0.1,length=1024)
        
        sys.density['A'] = 0.45
        sys.density['B'] = 0.35
        
        sys.closure.setUnset(typyPRISM.closure.PercusYevick())
        
        sys.potential.setUnset(typyPRISM.potential.HardSphere(sigma=1.0))
        
        sys.omega['A','A'] = typyPRISM.omega.SingleSite()
        sys.omega['A','B'] = typyPRISM.omega.NoIntra()
        sys.omega['B','B'] = typyPRISM.omega.Gaussian(sigma=1.0,length=100)
        
        PRISM = sys.createPRISM()
        
        self.assertIsInstance(PRISM,typyPRISM.core.PRISM.PRISM)
        
    def test_createDensityMatrices(self):
        '''Can we construct the two necesssary density matrices?'''
        sys = typyPRISM.System(['A','B'])
        
        sys.density['A'] = rhoA = 0.45
        sys.density['B'] = rhoB = 0.35
        
        siteDensityMatrix1 = np.zeros((2,2))
        siteDensityMatrix1[0,0] = rhoA
        siteDensityMatrix1[0,1] = rhoA + rhoB
        siteDensityMatrix1[1,0] = rhoA + rhoB
        siteDensityMatrix1[1,1] = rhoB
        
        pairDensityMatrix1 = np.zeros((2,2))
        pairDensityMatrix1[0,0] = rhoA * rhoA
        pairDensityMatrix1[0,1] = rhoA * rhoB
        pairDensityMatrix1[1,0] = rhoB * rhoA
        pairDensityMatrix1[1,1] = rhoB * rhoB
        
        siteDensityMatrix2,pairDensityMatrix2 = sys.createDensityMatrices()
        
        np.testing.assert_array_almost_equal(siteDensityMatrix1,siteDensityMatrix2)
        np.testing.assert_array_almost_equal(pairDensityMatrix1,pairDensityMatrix2)
        
        
        
         
        