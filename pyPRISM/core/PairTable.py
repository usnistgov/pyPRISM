from pyPRISM.core.Table import Table
from pyPRISM.core.MatrixArray import MatrixArray
from pyPRISM.core.Space import Space
from itertools import product
import numpy as np
import copy

class PairTable(Table):
    '''Container for data that is keyed by pairs of types

    **Description**

        Since PRISM is a theory based in *pair*-correlation functions, it
        follows that many of the necessary parameters of the theory are
        specified between the pairs of types. This goal of this container is to
        make setting, getting, and checking these data easy.
        
        Setter/getter methods have been set up to set groups of types
        simultaneously. This allows for the rapid construction of datasets
        where many of the parameters are repeated. This class also
        automatically assumes pair-reversibility and handles the setting of
        unlike pairs automatically i.e. A-B and B-A are set at the same time.

        Note that, unlike the :class:`pyPRISM.core.MatrixArray`, this
        container is not meant to be used for mathematics. The benefit of this
        is that, for each type, it can contain any arbitrary number, string, or
        Python object. 

        See the example below and the `pyPRISM Internals` section of the
        :ref:`tutorial` for more information.

    Example
    -------
    .. code-block:: python

        import pyPRISM

        PT = pyPRISM.PairTable(['A','B','C'],name='potential')

        # Set the 'A-A' pair
        PT['A','A']            = 'Lennard-Jones'

        # Set the 'B-A', 'A-B', 'B-B', 'B-C', and 'C-B' pairs
        PT['B',['A','B','C'] ] = 'Weeks-Chandler-Andersen'

        # Set the 'C-A', 'A-C', 'C-C' pairs
        PT['C',['A','C'] ]     = 'Exponential'

        for i,t,v in PT.iterpairs():
            print('{}) {} for pair {}-{} is {}'.format(i,VT.name,t[0],t[1],v))

        # The above loop prints the following:
        #   (0, 0)) potential for pair A-A is Lennard-Jones
        #   (0, 1)) potential for pair A-B is Weeks-Chandler-Andersen
        #   (0, 2)) potential for pair A-C is Exponential
        #   (1, 1)) potential for pair B-B is Weeks-Chandler-Andersen
        #   (1, 2)) potential for pair B-C is Weeks-Chandler-Andersen
        #   (2, 2)) potential for pair C-C is Exponential

        for i,t,v in PT.iterpairs(full=True):
            print('{}) {} for pair {}-{} is {}'.format(i,VT.name,t[0],t[1],v))

        # The above loop prints the following:
        #   (0, 0)) potential for pair A-A is Lennard-Jones
        #   (0, 1)) potential for pair A-B is Weeks-Chandler-Andersen
        #   (0, 2)) potential for pair A-C is Exponential
        #   (1, 0)) potential for pair B-A is Weeks-Chandler-Andersen
        #   (1, 1)) potential for pair B-B is Weeks-Chandler-Andersen
        #   (1, 2)) potential for pair B-C is Weeks-Chandler-Andersen
        #   (2, 0)) potential for pair C-A is Exponential
        #   (2, 1)) potential for pair C-B is Weeks-Chandler-Andersen
        #   (2, 2)) potential for pair C-C is Exponential

    
    
    '''
    def __init__(self,types,name,symmetric=True):
        r'''Constructor

        Arguments
        ----------
        types: list
            Lists of the types that will be used to key the PairTable. The length of this
            list should be equal to the rank of the PRISM problem to be solved, i.e. 
            len(types) == number of sites in system
            
        name: string
            The name of the PairTable. This is simply used as a convencience for identifying
            the table internally. 
        
        symmetric: bool
            If *True*, the table will automatically set both off-diagonal values during
            assignment e.g. PT['A','B'] = 5 will set 'A-B' and 'B-A'
        '''
        self.types = types
        self.symmetric = symmetric
        self.name = name
        self.values = {t1:{t2:None for t2 in types} for t1 in types}
    
    def __repr__(self):
        return '<PairTable: {}>'.format(self.name)
        
    def __iter__(self):
        for (i,t1),(j,t2) in product(enumerate(self.types),enumerate(self.types)):
            yield (i,j),(t1,t2),self.values[t1][t2]
            
    def __getitem__(self,index):
        t1,t2 = index
        return self.values[t1][t2]
    
    def __setitem__(self,index,value):
        types1,types2 = index
        for t1 in self.listify(types1):
            for t2 in self.listify(types2):
                
                # If we don't copy the value, later modifications to this element
                # can affect all other set items. While this could be used intentionally,
                # it negates a primary use case of setting a global "default" value across
                # the table and then only modifying specific elements afterwards
                value_copy = copy.deepcopy(value) 
                
                self.values[t1][t2] = value_copy
                if self.symmetric and t1!=t2:
                    self.values[t2][t1] = value_copy
            
    def check(self):
        '''Is everything in the table set?

        Raises
        ------
        ValueError if all values are not set
        
        '''
        for i,t,val in self.iterpairs():
            if val is None:
                raise ValueError('PairTable {} is not fully specified!'.format(self.name))
            
            
    def iterpairs(self,full=False,diagonal=True):
        '''Convenience function for looping over table pairs.
        
        Parameters
        ----------
        full: bool
            If *True*, all i,j pairs (upper and lower diagonal) will be looped over
            
        diagonal: bool
            If *True*, only the i==j (on-diagonal) pairs will be considered when looping
        
        '''
        
        if full:
            test = lambda i,j: True
        elif diagonal:
            test = lambda i,j: i<=j
        else:
            test = lambda i,j: i<j
            
        for (i,j),(t1,t2),val in self.__iter__():
            if test(i,j):
                yield (i,j),(t1,t2),(val)
                
    def setUnset(self,value):
        '''Set all values that have not been specified to a value

        Arguments
        ---------
        value: 
            Any valid python object (number, list, array, etc) can be passed in
            as a value for all unset fields. 
        
        '''
        for i,(t1,t2),v in self.iterpairs():
            if v is None:
                self[t1,t2] = value
                
    def exportToMatrixArray(self,space=Space.Real):
        '''Convenience function for converting a table of arrays to a MatrixArray

        .. warning::

            This only works if the PairTable contains numerical data that is
            all of the same shape that can be cast into a np.ndarray like
            object.
        
        '''
        lengths = []
        for i,t,val in self.iterpairs():
            if val is None:
                raise ValueError('Can\'t export not-fully specified Table {}'.format(self.name))
            lengths.append(len(val))
            
        if not len(set(lengths))<=1:
            raise ValueError('Arrays in Table are not all the same length. Aborting export.')
        
        length = lengths[0]
        rank = len(self.types)
        MA = MatrixArray(length=length,rank=rank,space=space,types=self.types)
        
        for i,(t1,t2),val in self.iterpairs():
            MA[t1,t2] = val
        return MA
    
    def apply(self,func,inplace=True):
        '''Apply a function to all elements in the table in place
        
        Parameters
        ----------
        func: any object with __call__ method
            function to be called on all table elements

        inplace: bool
            If *True*, apply modifications to self. Otherwise, create a new PairTable.
        
        '''
        if inplace:
            table = self
        else:
            table = PairTable(types=self.types,name=self.name,symmetric=self.symmetric)
            
        for i,(t1,t2),val in self.iterpairs():
            table[t1,t2] = func(val)
            
        return table
        

        
