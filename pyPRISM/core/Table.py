class Table:
    '''Baseclass used to define tables of parameters
    
    This class should not be used/instatiated directly. It is intended to be
    only inherited.
    
    '''
    def listify(self,values):
        '''Helper fuction that converts any input into a list of inputs.
        
        The purpose of this function is to help with iterating over types,
        and handling the case of a single "str" type being passed. 
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
        
