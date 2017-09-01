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
        
        
