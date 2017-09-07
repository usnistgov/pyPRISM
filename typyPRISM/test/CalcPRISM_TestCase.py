#!python
from __future__ import division,print_function
import typyPRISM
import numpy as np
import unittest

class CalcPRISM_TestCase(unittest.TestCase):
    def setup(self):
        '''Construct a simple but fully specified PRISM problem'''
        
        sys = typyPRISM.System(['A','B'])
        
        sys.domain = typyPRISM.Domain(dr=0.1,length=1024)
        
        sys.density['A'] = 0.1
        sys.density['B'] = 0.75
        
        sys.closure.setUnset(typyPRISM.closure.PercusYevick())
        
        sys.potential.setUnset(typyPRISM.potential.HardSphere(sigma=1.0))
        
        sys.omega['A','A'] = typyPRISM.omega.SingleSite()
        sys.omega['A','B'] = typyPRISM.omega.NoIntra()
        sys.omega['B','B'] = typyPRISM.omega.Gaussian(sigma=1.0,length=10000)
        
        PRISM = sys.createPRISM()
        
        return PRISM

    def test_pair_correlation(self):
        '''Can we calculate pair_correlations?'''
        PRISM = self.setup()
        PRISM.solve(disp=False)
        result = typyPRISM.calculate.prism.pair_correlation(PRISM)
        
    def test_structure_factor(self):
        '''Can we calculate structure factors?'''
        PRISM = self.setup()
        PRISM.solve(disp=False)
        result = typyPRISM.calculate.prism.structure_factor(PRISM)
        
    def test_pmf(self):
        '''Can we calculate pmf's?'''
        PRISM = self.setup()
        PRISM.solve(disp=False)
        result = typyPRISM.calculate.prism.pmf(PRISM)
        
    def test_chi(self):
        '''Can we calculate chi's?'''
        PRISM = self.setup()
        PRISM.solve(disp=False)
        result = typyPRISM.calculate.prism.chi(PRISM)

    def test_second_virial(self):
        '''Can we calculate B2's?'''
        PRISM = self.setup()
        PRISM.solve(disp=False)
        result = typyPRISM.calculate.prism.second_virial(PRISM)

    def test_solvation_potential(self):
        '''Can we calculate psi?'''
        PRISM = self.setup()
        PRISM.solve(disp=False)
        result = typyPRISM.calculate.prism.solvation_potential(PRISM)
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CalcPRISM_TestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
