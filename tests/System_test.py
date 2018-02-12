#!python
from __future__ import division,print_function
import pyPRISM
import unittest
import numpy as np

class System_TestCase(unittest.TestCase):
    def test_create(self):
        '''Can we create a system?'''
        types = ['A','B','C']
        sys = pyPRISM.System(types)
    def test_check(self):
        '''Can we validate a system object?'''
        types = ['A','B','C']
        sys = pyPRISM.System(types)
        self.assertRaises(ValueError,sys.check)
        
        # These values make no sense but their sufficient
        # for this 'check'
        sys.domain = pyPRISM.Domain(dr=0.1,length=1024)
        sys.density[sys.types] = 1.0
        sys.diameter[sys.types] = 1.0
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
        
        sys = pyPRISM.System(['A','B'])
        
        sys.domain = pyPRISM.Domain(dr=0.1,length=1024)
        
        sys.density['A'] = 0.45
        sys.density['B'] = 0.35

        sys.diameter[sys.types] = 1.0
        
        sys.closure.setUnset(pyPRISM.closure.PercusYevick())
        
        sys.potential.setUnset(pyPRISM.potential.HardSphere(sigma=1.0))
        
        sys.omega['A','A'] = pyPRISM.omega.SingleSite()
        sys.omega['A','B'] = pyPRISM.omega.NoIntra()
        sys.omega['B','B'] = pyPRISM.omega.Gaussian(sigma=1.0,length=100)
        
        PRISM = sys.createPRISM()
        
        self.assertIsInstance(PRISM,pyPRISM.core.PRISM.PRISM)
        
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(System_TestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
