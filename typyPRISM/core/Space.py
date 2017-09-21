#!python
from enum import Enum

class Space(Enum):
    ''' An enumeration to track which space an object is in

    MatrixArrays can represent data in Real- or Fourier- space and they can be
    transformed in-place between these spaces. This class is meant to help
    track this state by creating a standard numerical reference for each state
    that can be checked. This allows classes like
    :class:`typyPRISM.core.MatrixArray` to do error checking when doing math
    between arrays to make sure we don't multiply two arrays that aren't in the
    same space.  This enumeration also defines a 'wildcard' state so that we
    can still do math with non-spatial data. 

    Example
    -------
    .. code-block:: python
        
        import typyPRISM

        A = typyPRISM.MatrixArray(length=1000,rank=3,space=typyPRISM.Space.Real)
        B = typyPRISM.MatrixArray(length=1000,rank=3,space=typyPRISM.Space.Real)
        C = typyPRISM.MatrixArray(length=1000,rank=3,space=typyPRISM.Space.Fourier)

        A.space == B.Space # returns True
        A.space == C.Space # returns False

        A.dot(C) #raises exception 
    '''
    Real       = 1
    Fourier    = 2
    NonSpatial = 3
