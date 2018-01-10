#!python
from __future__ import division,print_function
import unittest
import numpy as np
try:
    from pyPRISM.trajectory import Debyer
except ImportError:
    exit(0)
from pyPRISM import Domain



class Debyer_TestCase(unittest.TestCase):
    def setup_rod(self,Nf,N):
        positions = []
        for j in range(Nf):
            dummy = []
            for i in range(N):
                dummy.append([0.0,0.0,i])
            positions.append(dummy)
        positions = np.array(positions)
        molecules = np.zeros(N,dtype=int)
        box = np.repeat([[1000.,1000.,1000.]],Nf,axis=0)
        return positions,molecules,box
    def test_self_omega(self):
        '''Can we calculate a self-omega?'''

        domain = Domain(dk = 0.1, length = 1024)
        debyer = Debyer(domain=domain,nthreads=2)

        Nf = 1
        N = 50
        positions,molecules,box = self.setup_rod(Nf,N)

        selfHist = True
        omega = debyer.calculate(positions,positions,
                                 molecules,molecules,
                                 box,
                                 selfHist)

        k, omega_control = np.loadtxt('data/omega.1rod.dat')
        np.testing.assert_array_almost_equal(omega,omega_control,decimal=3)
    def test_non_self_omega(self):
        '''Can we calculate a non-self omega?'''

        domain = Domain(dk = 0.1, length = 1024)
        debyer = Debyer(domain=domain,nthreads=2)

        Nf = 1
        N = 50
        positions,molecules,box = self.setup_rod(Nf,N)

        mask1 = (np.arange(N)<(N//2))
        mask2 = (np.arange(N)>=(N//2))

        positions1 = positions[:,mask1,:]
        positions2 = positions[:,mask2,:]
        molecules1 = molecules[mask1]
        molecules2 = molecules[mask2]

        selfHist = False
        omega = debyer.calculate(positions1,positions2,
                                 molecules1,molecules2,
                                 box,
                                 selfHist)

        k, omega_control = np.loadtxt('data/omega.2rod.dat')
        np.testing.assert_array_almost_equal(omega,omega_control)

        

        
if __name__ == '__main__':
    import unittest 
    suite = unittest.TestLoader().loadTestsFromTestCase(Debyer_TestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
