#!python
from __future__ import division,print_function
import unittest
import numpy as np
import pyPRISM

class PRISM_TestCase(unittest.TestCase):
    def setup(self):
        '''Construct a simple but fully specified PRISM problem'''
        
        sys = pyPRISM.System(['A','B'])
        
        sys.domain = pyPRISM.Domain(dr=0.1,length=1024)
        
        sys.density['A'] = 0.2
        sys.density['B'] = 0.6

        sys.diameter[sys.types] = 1.0
        
        sys.closure[sys.types,sys.types] = pyPRISM.closure.PercusYevick()
        
        sys.potential[sys.types,sys.types] = pyPRISM.potential.HardSphere(sigma=1.0)
        
        sys.omega['A','A'] = pyPRISM.omega.SingleSite()
        sys.omega['A','B'] = pyPRISM.omega.NoIntra()
        sys.omega['B','B'] = pyPRISM.omega.Gaussian(sigma=1.0,length=10000)
        
        PRISM = sys.createPRISM()
        
        return PRISM
    def test_solve(self):
        '''Can we solve the PRISM equations?'''
        PRISM = self.setup()
        result = PRISM.solve(options={'disp':False})
        self.assertIsNot(result,None)
        
        
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(PRISM_TestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
