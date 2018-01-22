from pyPRISM.core.Table import Table
import numpy as np

class ValueTable(Table):
    '''Container for data that is keyed by types


    **Description**

        The goal of this class is to provide a simple inteface for setting and
        storing parameters that are accessed and identified by types. This is
        typically site properties, e.g. density, site diameter. By default the
        value for all types is set to `None` and therefore can be checked to see
        if the table has been fully specified. 

        Setter/getter methods have been create to set groups of types
        simultaneously. This allows for the rapid construction of datasets
        where many of the parameters are repeTated. 

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

        VT = pyPRISM.ValueTable(['A','B','C','D','E'],name='density')

        # set the value for type A to be 0.25
        VT['A'] = 0.25

        # set the value for types B & C to be 0.35
        VT[ ['B','C'] ] = 0.35

        # set all other values to be 0.1
        VT.setUnset(0.1)

        for i,t,v in VT:
            print('{}) {} for type {} is {}'.format(i,VT.name,t,v))


        # The above loop prints the following:
        #   0) density for type A is 0.25
        #   1) density for type B is 0.35
        #   2) density for type C is 0.35
        #   3) density for type D is 0.1
        #   4) density for type E is 0.1
    
    
    '''
    def __init__(self,types,name):
        r'''Constructor
        
        Arguments
        ---------
        types: list
            Lists of the types that will be used to key the ValueTable. The
            length of this list should be equal to the rank of the PRISM
            problem to be solved i.e.  len(types) == number of sites in system.
            
        name: string
            The name of the ValueTable. Currently, this is simply used as a
            convencience for identifying the table internally. 
        '''

        self.types = types
        self.name = name
        self.values = {t:None for t in types}
    
    def __repr__(self):
        return '<ValueTable: {}>'.format(self.name)
        
    def __iter__(self):
        '''Data iterator

        This magic-method allows for ValueTables to be iterated over via
        `for x in y` constructs like

        .. code-block:: python

            for index,type,value in ValueTable: 
                print(index,type,value)

        Yields
        ------
        index: int
            index of value

        type: 
            type of value

        value: 
            stored value at this type
        '''
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
        '''Is everything in the table set?

        Raises
        ------
        *ValueError* if all values are not set
        
        '''
        for i,t,val in self:
            if val is None:
                raise ValueError('ValueTable {} is not fully specified!'.format(self.name))
            
            
    def setUnset(self,value):
        '''Set all values that have not been specified to a value

        Arguments
        ---------
        value: 
            Any valid python object (number, list, array, etc) can be passed in
            as a value for all unset fields. 
        
        '''
        for i,t,v in self:
            if v is None:
                self[t] = value
