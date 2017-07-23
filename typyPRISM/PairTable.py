from Table import Table
from math import sqrt
import operator

class PairTable(Table):
  def __init__(self,types,parms,symmetric=True):
    self.symmetric = symmetric
    base_table = {t1:{t2:None for t2 in types} for t1 in types}
    super(PairTable,self).__init__(types,parms,base_table)
  def __iter__(self):
    for t1,t2 in self.pairs:
      valueDict = {}
      valueDict['t1'] = t1
      valueDict['t2'] = t2
      valueDict['n1'] = self.A2N[t1]
      valueDict['n2'] = self.A2N[t2]
      for parm in self.parms:
        valueDict[parm] = self.values[parm][t1][t2]
      yield valueDict
  def __getitem__(self,idex):
    if idex in self.parms:
      return self.values[idex]
    elif len(idex)==3:
      parm = idex[0]
      inum,ialph = self.ParseValue(idex[1])
      jnum,jalph = self.ParseValue(idex[2])
      return self.values[parm][ialph][jalph]
    else:
      raise TypeError('PairTable[#] (i.e. __getitem__) needs either 1 or 3 arguments')
  def __setitem__(self,idex,value):
    if len(idex)<3:
      raise AttributeError('PairTable[#] (i.e. __setitem__) needs at least 4 arguments')
    parm = idex[0]
    if not (parm in self.parms):
      raise ValueError('Parameter {} doesn\'t exist in this PairTable!'.format(parm))
    inum,ialph = self.ParseValue(idex[1])
    jnum,jalph = self.ParseValue(idex[2])
    self.values[parm][ialph][jalph] = value
    if self.symmetric and ialph!=jalph:
      self.values[parm][jalph][ialph] = value
  def check(self,parms=None,raiseException=True):
    parms = self.ParseParms(parms)
    checks = []
    for p in parms:
      for t1,t2 in self.all_pairs:
        checks.append(self.values[p][t1][t2] is not None)
    if raiseException and not all(checks):
      raise ValueError('PairTable check failed. Not all pairs set!')
    else:
      return checks
  def echo(self,parms=None):
    parms = self.ParseParms(parms)

    print 'Types'
    for t1 in self.types:
      for t2 in self.types:
        print '{:5s}'.format(t1+t2),' ',
      print ''
    print ''

    for parm in parms:
      print parm
      for t1 in self.types:
        for t2 in self.types:
          val = self.values[parm][t1][t2]
          try:
            val = float(val)
            print '{:4.3f}'.format(val),' ',
          except ValueError:
            print '{:5s}'.format(str(val)),' ',
        print ''
      print ''
    print ''
  def setUnsetValues(self,parm,value):
    if not (parm in self.parms):
      raise ValueError('Parameter {} doesn\'t exist in this PairTable!'.format(parm))
    for i,j in self.pairs:
      if self.values[parm][i][j] is None:
        self.values[parm][i][j] = value
        if self.symmetric and i!=j:
          self.values[parm][j][i] = value
  def setConditionally(self,setParm,setValue,checkParm,checkValue,comparison=operator.eq):
    if not (setParm in self.parms):
      raise ValueError('Parameter {} doesn\'t exist in this PairTable!'.format(setParm))
    if not (checkParm in self.parms):
      raise ValueError('Parameter {} doesn\'t exist in this PairTable!'.format(checkParm))
    for i,j in self.pairs:
      if comparison(self.values[checkParm][i][j],checkValue):
        self.values[setParm][i][j] = setValue
        if self.symmetric and i!=j:
          self.values[setParm][j][i] = setValue
  def mix(self,parms,rule='arithmetic'):
    parms = self.ParseParms(parms)

    if rule=='arithmetic':
      mixr = lambda x1,x2: (x1+x2)/2.0
    elif rule=='geometric':
      mixr = lambda x1,x2: sqrt(x1*x2)/2.0
    else:
      raise ValueError('Mixing rule not recognized: {}'.format(rule))

    for parm in parms:
      #Need to make sure that all self values are set for this parm
      for t1 in self.types:
        val = self.values[parm][t1][t1]
        if val is None:
          raise ValueError('All diagonal-values (self-pairs) must be set before mixing!')
      for t1,t2 in self.off_diagonal_pairs:
        val1 = self.values[parm][t1][t1]
        val2 = self.values[parm][t2][t2]
        self.values[parm][t1][t2] = mixr(val1,val2)
        self.values[parm][t2][t1] = mixr(val1,val2)
  def get_matrix(self,parm,dtype=float):
    N = len(self.types)
    matrix = [[None for i in range(N)] for j in range(N)]
    for t1,t2 in self.pairs:
      n1 = self.A2N[t1]
      n2 = self.A2N[t2]
      matrix[n1][n2] = self.values[parm][t1][t2]
      matrix[n2][n1] = self.values[parm][t2][t1]
    return matrix
