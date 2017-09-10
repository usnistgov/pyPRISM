#!python
from __future__ import division,print_function
from typyPRISM.core.ValueTable import ValueTable
from typyPRISM.core.PairTable import PairTable
from typyPRISM.core.MatrixArray import MatrixArray
from typyPRISM.core.Space import Space
import numpy as np

class Density(object):
    '''Container for site and pair densities
    
    Density describes the makeup of the system in terms of both
    total site and pair densities
    
    Attributes
    ----------
    density: typyPRISM.ValueTable
        Table of site number density values

    total: float
        Total number density 

    site: typyPRISM.MatrixArray
        Total site density for each pair. For i == j, the site_density =
        rho_i, for i != j site_density = rho_i + rho_j

    pair: typyPRISM.MatrixArray
        Pair site density for each pair.  pair_density = rho_i * rho_j
    
    '''
    def __init__(self,types):
        self.types = types 

        self.density = ValueTable(types=types,name='density')
        self.total = 0.

        self.pair = MatrixArray(length=1,rank=len(types),types=types,space=Space.NonSpatial)
        self.site = MatrixArray(length=1,rank=len(types),types=types,space=Space.NonSpatial)

    def check(self):
        '''Are all densities set?'''
        self.density.check()

    def __repr__(self):
        return '<Density total:{:3.2f}>'.format(self.total)

    def __getitem__(self,key):
        return self.density[key]

    def __setitem__(self,t1,value):
        rho1 = value
        self.density[t1] = rho1

        self.total = 0.
        for t2 in self.types:
            # If rho2 isn't set yet, we can't set the
            # site or pair densities
            rho2 = self.density[t2]
            if rho2 is None:
                continue

            self.total += rho2

            # The values must be set as lists in order for them to
            # be compatible with the MatrixArray type
            self.pair[t1,t2] = [rho1*rho2]
            if t1 == t2:
                self.site[t1,t2] = [rho1]
            else:
                self.site[t1,t2] = [rho1 + rho2]
