from typyPRISM.core.Table import Table
import numpy as np

class ValueTable(Table):
    '''Container for data that is keyed by types
    
    Parameters
    ----------
    types: list
        Lists of the types that will be used to key the ValueTable. The length of this
        list should be equal to the rank of the PRISM problem to be solved i.e. 
        len(types) == number of sites in system
        
    name: string
        The name of the ValueTable. This is simply used as a convencience for identifying
        the table internally. 
    
    
    '''
    def __init__(self,types,name):
        self.types = types
        self.name = name
        self.values = {t:None for t in types}
    
    def __repr__(self):
        return '<ValueTable: {}>'.format(self.name)
        
    def __iter__(self):
        for i,t in enumerate(self.types):
            yield i,t,self.values[t]
            
    def __getitem__(self,index):
        t = index
        return self.values[t]
    
    def __setitem__(self,index,value):
        types1 = index
        for t in self.listify(types1):
            self.values[t] = value
            
    def check(self):
        '''Is everything in the table set?'''
        for i,t,val in self:
            if val is None:
                raise ValueError('ValueTable {} is not fully specified!'.format(self.name))
            
            
    def setUnset(self,value):
        '''Set all values that have not been specified to a value'''
        for i,t,v in self:
            if v is None:
                self[t] = value