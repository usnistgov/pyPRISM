class Table:
    '''Baseclass used to define tables of parameters
    
    .. note::

        This class should not be used/instatiated directly. It is only intended to be
        inherited.
    
    '''
    def listify(self,values):
        '''Helper fuction that converts any input into a list of inputs.
        
        The purpose of this function is to help with iterating over types,
        and to handle the case of a single :class:`str` type being passed. 
        '''
        if isinstance(values,str):
            values = [values]
        else:
            try:
                iter(values)
            except TypeError:
                values = [values]
            else:
                values = list(values)
        return values
        
