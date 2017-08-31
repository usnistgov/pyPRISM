#!python
from __future__ import division,print_function
import unittest
import numpy as np
import typyPRISM

class PRISM_TestCase(unittest.TestCase):
    def setup(self):
        '''Construct a simple but fully specified PRISM problem'''
        
        sys = typyPRISM.System(['A','B'])
        
        sys.domain = typyPRISM.Domain(dr=0.1,length=1024)
        
        sys.density['A'] = 0.2
        sys.density['B'] = 0.6
        
        sys.closure[sys.types,sys.types] = typyPRISM.closure.PercusYevick()
        
        sys.potential[sys.types,sys.types] = typyPRISM.potential.HardSphere(sigma=1.0)
        
        sys.omega['A','A'] = typyPRISM.omega.SingleSite()
        sys.omega['A','B'] = typyPRISM.omega.NoIntra()
        sys.omega['B','B'] = typyPRISM.omega.Gaussian(sigma=1.0,length=10000)
        
        PRISM = sys.createPRISM()
        
        return PRISM
    def test_solve(self):
        '''Can we solve the PRISM equations?'''
        PRISM = self.setup()
        result = PRISM.solve(disp=False)
        self.assertIsNot(result,None)
        
        
        
if __name__ == '__main__':
    suite_list = []
    suite_list.append(unittest.TestLoader().loadTestsFromTestCase(PRISM_TestCase))
    suite = unittest.TestSuite(suite_list)
    unittest.TextTestRunner(verbosity=2).run(suite)
