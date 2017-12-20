#!python
from __future__ import division,print_function
import pyPRISM
import numpy as np
import unittest

class CalcPRISM_TestCase(unittest.TestCase):
    def setup(self):
        '''Construct a simple but fully specified PRISM problem'''
        
        sys = pyPRISM.System(['A','B'])
        
        sys.domain = pyPRISM.Domain(dr=0.1,length=1024)
        
        sys.density['A'] = 0.1
        sys.density['B'] = 0.75

        sys.diameter[sys.types] = 1.0
        
        sys.closure.setUnset(pyPRISM.closure.PercusYevick())
        
        sys.potential.setUnset(pyPRISM.potential.HardSphere(sigma=1.0))
        
        sys.omega['A','A'] = pyPRISM.omega.SingleSite()
        sys.omega['A','B'] = pyPRISM.omega.NoIntra()
        sys.omega['B','B'] = pyPRISM.omega.Gaussian(sigma=1.0,length=10000)
        
        PRISM = sys.createPRISM()
        
        return PRISM

    def test_pair_correlation(self):
        '''Can we calculate pair_correlations?'''
        PRISM = self.setup()
        PRISM.solve(options={'disp':False})
        result = pyPRISM.calculate.pair_correlation(PRISM)
        
    def test_structure_factor(self):
        '''Can we calculate structure factors?'''
        PRISM = self.setup()
        PRISM.solve(options={'disp':False})
        result = pyPRISM.calculate.structure_factor(PRISM)
        
    def test_pmf(self):
        '''Can we calculate pmf's?'''
        PRISM = self.setup()
        PRISM.solve(options={'disp':False})
        result = pyPRISM.calculate.pmf(PRISM)

    def test_chi(self):
        '''Can we calculate chi's?'''
        PRISM = self.setup()
        PRISM.solve(options={'disp':False})
        result = pyPRISM.calculate.chi(PRISM)

    def test_second_virial(self):
        '''Can we calculate B2's?'''
        PRISM = self.setup()
        PRISM.solve(options={'disp':False})
        result = pyPRISM.calculate.second_virial(PRISM)

    def test_solvation_potential(self):
        '''Can we calculate psi?'''
        PRISM = self.setup()
        PRISM.solve(options={'disp':False})
        result = pyPRISM.calculate.solvation_potential(PRISM)

    def test_spinodal(self):
        '''Can we calculate spinodal conditions?'''
        PRISM = self.setup()
        PRISM.solve(options={'disp':False})
        result = pyPRISM.calculate.spinodal_condition(PRISM)
        
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CalcPRISM_TestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
