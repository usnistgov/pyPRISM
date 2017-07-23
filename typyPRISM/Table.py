import copy

class Table(object):
  def __init__(self,types,parms,base_table):
    self.parms =  parms
    self.values = {p:copy.deepcopy(base_table) for p in parms}
    A2N = {}; N2A = {};
    for n,t in enumerate(types,start=0):
      #We want the 'types' to be non-int like (i.e. not-castable to int)
      #With this assumption, we can handle '1' and 1 as 
      # being equivalent "numeric" types (i.e. LAMMPS types)
      try:
        int(t)
      except ValueError:
        pass
      else:
        raise TypeError('Types cannot be castable to int!')
      A2N[t] = n
      N2A[n] = t
    # A2N['NoType'] = 0 #add default "no-type'
    # N2A[0] = 'NoType'
    self.A2N = A2N #alpha-type to numeric-type mapping
    self.N2A = N2A #numeric-type to alpha-type mapping
    self.types = types
    self.numericTypes = [A2N[t] for t in types]
    self.pairs = []
    self.all_pairs = []
    self.off_diagonal_pairs = []
    for i in self.numericTypes:
      for j in self.numericTypes:
        self.all_pairs.append([N2A[i],N2A[j]])
        if i<=j:
          self.pairs.append([N2A[i],N2A[j]])
        if i!=j:
          self.off_diagonal_pairs.append([N2A[i],N2A[j]])
  def ParseValue(self,val):
    '''
    Make sure that we are always returning a str-like typeo
    '1' will be converted to int(1) and then parsed using N2A
    '''
    try:
      numericValue=int(val)
      if not numericValue in self.numericTypes:
        raise KeyError('Numeric Type {} not in Table!'.format(numericValue))
      alphaValue=self.N2A[numericValue]
    except ValueError:
      alphaValue = val
      if not alphaValue in self.types:
        raise KeyError('Alpha Type {} not in Table!'.format(alphaValue))
      numericValue=self.A2N[alphaValue]
    return numericValue,alphaValue
  def ParseParms(self,parms=None):
    if parms is None:
      parms = self.parms
    elif not (isinstance(parms,list) or isinstance(parms,tuple)):
      parms = [parms]
    for parm in parms:
      if not (parm in self.parms):
        raise ValueError('Parameter {} doesn\'t exist in this Table!'.format(parm))
    return parms
