from typyPRISM.core.Table import Table
from typyPRISM.core.MatrixArray import MatrixArray
from typyPRISM.core.Space import Space
from itertools import product
import numpy as np

class PairTable(Table):
    '''Container for data that is keyed by pairs of types
    
    Since PRISM is a theory based in *pair*-correlation functions, it 
    follows that many of the necessary parameters of the theory are specified
    between the pairs of types. This goal of this container is to make setting,
    getting, and checking these data easy.
    
    To start, setter/getter methods have been set up to set groups of types 
    simultaneously. For example::
        
            PT = PairTable(['A','B','C','D'],'density',symmetric=True)
            
            # The following sets the 'A-C' and 'B-C' pairs to be 0.5. Also, since
            # we set symmetric=True above, 'C-A' and 'C-B' is also set
            PT[['A','B'],'['C']] = 0.5
    
    This allows for the rapid construction of datasets where many of the parameters
    are repeated. 
    
    Parameters
    ----------
    types: list
        Lists of the types that will be used to key the PairTable. The length of this
        list should be equal to the rank of the PRISM problem to be solved i.e. 
        len(types) == number of sites in system
        
    name: string
        The name of the PairTable. This is simply used as a convencience for identifying
        the table internally. 
    
    symmetric: bool
        If True, the table will automatically set both off-diagonal values during
        assignment e.g. PT['A','B'] = 5 will set 'A-B' and 'B-A'
    

    
    '''
    def __init__(self,types,name,symmetric=True):
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
                self.values[t1][t2] = value
                if self.symmetric and t1!=t2:
                    self.values[t2][t1] = value
            
    def check(self):
        '''Is everything in the table set?'''
        for i,t,val in self.iterpairs():
            if val is None:
                raise ValueError('PairTable {} is not fully specified!'.format(self.name))
            
            
    def iterpairs(self,full=False,diagonal=True):
        '''Convenience function for looping over table pairs.
        
        Parameters
        ----------
        full: bool
            If True, all i,j pairs (upper and lower diagonal) will be looped over
            
        diagonal: bool
            If True, the i==j (on-diagonal) pairs will be considered when looping
        
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
        '''Set all values that have not been specified to a value'''
        for i,(t1,t2),v in self.iterpairs():
            if v is None:
                self[t1,t2] = value
                
    def exportToMatrixArray(self,space=Space.Real):
        '''Convenience function for converting a table of arrays to a MatrixArray'''
        lengths = []
        for i,t,val in self.iterpairs():
            if val is None:
                raise ValueError('Can\'t export not-fully specified Table {}'.format(self.name))
            lengths.append(len(val))
            
        if not len(set(lengths))<=1:
            raise ValueError('Arrays in Table are not all the same length. Aborting export.')
        
        length = lengths[0]
        rank = len(self.types)
        MA = MatrixArray(length=length,rank=rank,space=space)
        
        for (i,j),t,val in self.iterpairs():
            MA[i,j] = val
        return MA
    
    def apply(self,funk):
        '''Apply a function to all elements in the table in place
        
        Parameters
        ----------
        funk: any object with __call__ method
            function to be called on all table elements
        
        '''
        for i,(t1,t2),val in self.iterpairs():
            self[t1,t2] = funk(val)
        

        