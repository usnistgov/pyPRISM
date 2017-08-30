#!python
from __future__ import division,print_function
from typyPRISM.omega.Omega import Omega
import numpy as np

class FromFile(Omega):
    '''Read *intra*-molecular correlations from file
    
    This class reads a one or two column file using numpy's
    loadtxt function. A one-column file is expected to only
    contain intra-molecular correlation data, while a two-column
    file contains the k values of the data in the first column
    as well. If the k-values are provided, an extra check to make
    sure that the file data matches the same k-space grid of the
    domain is checked. 
    
    Attributes
    ----------
    fileName: str
        full path + name to column file
        
    '''
    def __init__(self,fileName):
        self.fileName = fileName
        
    def __repr__(self):
        return '<Omega: FromFile>'
    
    def calculate(self,k):
        fileData = np.loadtxt(self.fileName)
        
        if len(fileData.shape)>=2:
            assert fileData.shape[0] == k.shape[0],'Domain size of file differs from supplied domain!'
            assert (fileData[:,0] == k).all(),'Domain size of file differs from supplied domain!'
            self.value = fileData[:,1]
        else:
            self.value = fileData
        
        return self.value
        
        