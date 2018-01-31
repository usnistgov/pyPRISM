#!python
from __future__ import division,print_function
from pyPRISM.core.ValueTable import ValueTable
from pyPRISM.core.PairTable import PairTable
from pyPRISM.core.MatrixArray import MatrixArray
from pyPRISM.core.Space import Space
import numpy as np

class Density(object):
    r'''Container for pair and site densities

    **Mathematical Definition**

    .. math::
        
        \rho^{pair}_{\alpha,\beta} = \rho_{\alpha} \rho_{\beta} 

    .. math::
        
        \rho^{site}_{\alpha,\beta} = 
            \begin{cases}
                \rho_{\alpha}                & \text{if } i = j \\
                \rho_{\alpha} + \rho_{\beta} & \text{if } i \neq j
            \end{cases}

    .. math::
        
        \rho^{total} = \sum_{\alpha} \rho^{site}_{\alpha,\alpha}


    **Variable Definitions**

        :math:`\rho_{\alpha}`
            Number density of site :math:`\alpha`

        :math:`\rho^{pair}_{\alpha,\beta}`
            Pair number density of pair :math:`\alpha,\beta`

        :math:`\rho^{site}_{\alpha,\beta}`
            Site number density of pair :math:`\alpha,\beta`

        :math:`\rho^{total}`
            Total site number density 
        

    **Description**
    
        This class describes the makeup of the system in terms of both total
        site and pair densities. The container provides a simple interface for
        getting and setting (via square brackets [ ]) site densities and also
        takes care of calculating the total site and total pair number
        densities. The total site and pair number densities can be accessed as
        MatrixArrays (:class:`pyPRISM.core.MatrixArray`) attributes. 
    

    Example
    -------
    .. code-block:: python

        import pyPRISM

        rho = pyPRISM.Density(['A','B','C'])

        rho['A'] = 0.25
        rho['B'] = 0.35
        rho['C'] = 0.15

        rho.pair['A','B'] #pair density rho_AB = 0.25 * 0.35
        rho.site['A','B'] #site density rho_AB = 0.25 + 0.35
        rho.site['B','B'] #site density rho_BB = 0.35
        rho.total         #total density rho   = 0.25 + 0.35 + 0.15
    
    '''
    def __init__(self,types):
        r'''Constructor 

        Arguments
        ---------
        types: list 
            List of types of sites
        
        Attributes
        ----------
        density: :class:`pyPRISM.core.ValueTable`
            Table of site number density values

        total: float
            Total number density 

        site: :class:`pyPRISM.core.MatrixArray`
            Site density for each pair.

        pair: :class:`pyPRISM.core.MatrixArray`
            Pair site density for each pair.
        '''
        self.types = types 

        self.density = ValueTable(types=types,name='density')
        self.total = 0.

        self.pair = MatrixArray(length=1,rank=len(types),types=types,space=Space.NonSpatial)
        self.site = MatrixArray(length=1,rank=len(types),types=types,space=Space.NonSpatial)

    def check(self):
        '''Are all densities set?

        Raises
        ------
        *ValueError* if densities are not all set. 
        
        '''
        self.density.check()

    def __repr__(self):
        return '<Density total:{:3.2f}>'.format(self.total)

    def __getitem__(self,key):
        return self.density[key]

    def __setitem__(self,types1,value):
        for t1 in self.density.listify(types1):
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
