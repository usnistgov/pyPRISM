#!python
from __future__ import division,print_function
from pyPRISM.core.ValueTable import ValueTable
from pyPRISM.core.PairTable import PairTable
from pyPRISM.core.MatrixArray import MatrixArray
from pyPRISM.core.Space import Space
import numpy as np

class Diameter(object):
    r'''Container for site diameters and sigmas

    **Mathematical Definition**

    .. math::
        
        \sigma_{\alpha,\beta} = (d_{\alpha} + d_{\beta})/2.0
        

    **Variable Definitions**

        :math:`d_{\alpha}`
            diameter of site-type :math:`\alpha`

        :math:`sigma_{\alpha,\beta}`
            contact distanct between site-type :math:`\alpha` and :math:`\beta`

    **Description**

        A simple container class for defining the site-type diameters. 
    
    

    Example
    -------
    .. code-block:: python

        import pyPRISM

        d = pyPRISM.Diameter(['A','B','C'])

        d['A'] = 1.0
        d['B'] = 1.5
        d['C'] = 5.0

        d.diameter['A']  #site diameter diam_A = 1.0
        d.sigma['A','B'] #site contact distance sig_AB = 1.25
        d.sigma['A','C'] #site contact distance sig_AB = 3.0
    
    '''
    def __init__(self,types):
        r'''Constructor 

        Arguments
        ---------
        types: list 
            List of types of sites
        
        Attributes
        ----------
        diameter: :class:`pyPRISM.core.ValueTable`
            Table of site site diameter values

        volume: :class:`pyPRISM.core.ValueTable`
            Table of site site volumes values

        sigma: :class:`pyPRISM.core.PairTable`
            Site-site contact distance 
        '''
        self.types = types 

        self.diameter = ValueTable(types=types,name='diameter')
        self.volume = ValueTable(types=types,name='volume')
        self.sigma = PairTable(types=types,name='sigma')

    def check(self):
        '''Are all diameter set?

        Raises
        ------
        *ValueError* if diameters are not all set. 
        
        '''
        self.diameter.check()

    def __repr__(self):
        return '<Diameter>'

    def __getitem__(self,key):
        key = self.diameter.listify(key)
        if len(key) == 1:
            return self.diameter[key[0]]
        elif len(key) == 2:
            return self.sigma[key[0],key[1]]
        else:
            ValueError('Too many types passed to diameter!')

    def __setitem__(self,types1,value):
        for t1 in self.diameter.listify(types1):
            d1 = value
            self.diameter[t1] = d1

            self.volume[t1] = (4.0/3.0) * np.pi * (d1/2.0)**(3.0)

            self.total = 0.
            for t2 in self.types:
                # If d2 isn't set yet, we can't set sigma
                d2 = self.diameter[t2]
                if d2 is None:
                    continue

                self.sigma[t1,t2] = (d1 + d2)/2.0

