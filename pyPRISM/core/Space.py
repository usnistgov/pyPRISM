#!python

try:
    from enum import Enum
except ImportError:
    # Python 2.x
    parent = object
else:
    # Python 3.x
    parent = Enum


class Space(parent):
    ''' An enumeration to track which space an object is in

    **Description**
        MatrixArrays can represent data in Real- or Fourier- space and they can be
        transformed in-place between these spaces. This class is meant to help
        track this state by creating a standard numerical reference for each state
        that can be checked. This allows classes like
        :class:`pyPRISM.core.MatrixArray` to do error checking when doing math
        between arrays. This enumeration also defines a 'wildcard' state so that we
        can still do math with non-spatial data. 

    Example
    -------
    .. code-block:: python
        
        import pyPRISM

        A = pyPRISM.MatrixArray(length=1000,rank=3,space=pyPRISM.Space.Real)
        B = pyPRISM.MatrixArray(length=1000,rank=3,space=pyPRISM.Space.Real)
        C = pyPRISM.MatrixArray(length=1000,rank=3,space=pyPRISM.Space.Fourier)

        A.space == B.Space # returns True
        A.space == C.Space # returns False

        A.dot(C) #raises exception 

    .. note::

        The enumerated states of the Space Enum are listed below. The actual
        values of these states are not-important beyond being unique from one
        another.

    '''
    Real       = 1
    Fourier    = 2
    NonSpatial = 3
