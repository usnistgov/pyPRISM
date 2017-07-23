from Table import Table
import operator

class ValueTable(Table):
  def __init__(self,types,parms):
    base_table = {t1:None for t1 in types}
    super(ValueTable,self).__init__(types,parms,base_table)
  def __iter__(self):
    for t1 in self.types:
      valueDict = {}
      valueDict['t1'] = t1
      valueDict['n1'] = self.A2N[t1]
      for parm in self.parms:
        valueDict[parm] = self.values[parm][t1]
      yield valueDict
  def __getitem__(self,idex):
    if idex in self.parms:
      return self.values[idex]
    elif len(idex)==2:
      parm = idex[0]
      inum,ialph = self.ParseValue(idex[1])
      return self.values[parm][ialph]
    else:
      raise TypeError('ValueTable[#] (i.e. __getitem__) needs either 1 or 2 arguments')
  def __setitem__(self,idex,value):
    if len(idex)<2:
      raise AttributeError('ValueTable[#] (i.e. __setitem__) needs at least 3 arguments')
    parm = idex[0]
    if not (parm in self.parms):
      raise ValueError('Parameter {} doesn\'t exist in this ValueTable!'.format(parm))
    inum,ialph = self.ParseValue(idex[1])
    self.values[parm][ialph] = value
  def check(self,parms=None,raiseException=True):
    parms = self.ParseParms(parms)
    checks = []
    for p in parms:
      for t1 in self.types:
        checks.append(self.values[p][t1] is not None)
    if raiseException and not all(checks):
      raise ValueError('ValueTable check failed. Not all pairs set!')
    else:
      return checks
  def echo(self,parms=None):
    parms = self.ParseParms(parms)

    print 'Types',
    for t1 in self.types:
      print t1,' ',
    print ''

    for parm in parms:
      print parm,
      for t1 in self.types:
        print self.values[parm][t1],' ',
      print ''
    print ''
  def setUnsetValues(self,parm,value):
    if not (parm in self.parms):
      raise ValueError('Parameter {} doesn\'t exist in this ValueTable!'.format(parm))
    for i in self.types:
      if self.values[parm][i] is None:
        self.values[parm][i] = value
  def setConditionally(self,setParm,setValue,checkParm,checkValue,comparison=operator.eq):
    if not (setParm in self.parms):
      raise ValueError('Parameter {} doesn\'t exist in this ValueTable!'.format(setParm))
    if not (checkParm in self.parms):
      raise ValueError('Parameter {} doesn\'t exist in this ValueTable!'.format(checkParm))
    for i in self.types:
      if comparison(self.values[checkParm][i],checkValue):
        self.values[setParm][i] = setValue
