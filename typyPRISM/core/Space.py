#!python
from enum import Enum,auto

class Space(Enum):
    Real       = auto()
    Fourier    = auto()
    NonSpatial = auto()
