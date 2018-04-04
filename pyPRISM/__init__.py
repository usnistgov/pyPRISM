#!python
r'''
The fundamental PRISM equation is written in Fourier space as

.. math::
    \hat{H}(k) = \hat{\Omega}(k)\hat{C}(k) \left[\hat{\Omega}(k) + \hat{H}(k)\right]

where :math:`\hat{H}(k)` is the total correlation function,
:math:`\hat{\Omega}(k)` is the *intra*-molecular correlation function, and
:math:`\hat{C}(k)` is the direct correlation function. At each wavenumber
:math:`k`, each of these variables is an :math:`n \times n` matrix of values,
where :math:`n` is the number of components or site types in the system.  The
goal of any PRISM calculation is to obtain the full set of partial correlation
functions. Using these correlation functions, a number of structural and
thermodynamic properties can be calculated.

The :py:mod:`pyPRISM.core` module holds the fundamental data structures that
carry out the PRISM calculation.

The :py:mod:`pyPRISM.calculate` module provides a number of functions which use
*solved* :class:`pyPRISM.core.PRISM` objects to calculate structural and
thermodynamic parameters.

The :py:mod:`pyPRISM.closure` module provides closure objects which are necessary for
solving the PRISM equations.

The :py:mod:`pyPRISM.omega` module provides analytical *intra*-molecular
correlation (:math:`\hat{\omega}(k)`) functions along with methods for loading
them from memory or files.

The :py:mod:`pyPRISM.potential` module provides pair potentials for describing
the *inter*-molecular interactions in a system. Pairwise interactions are also
how the chemistry of the system is described.

The :py:mod:`pyPRISM.trajectory` module contains classes for working with
molecular simulation trajectories.

The :py:mod:`pyPRISM.util` module provides various global helper functions
which do not fall under the above categories.

See the :ref:`tutorial` for more information on the details of using pyPRISM
and the PRISM theory formalism.
'''
from pyPRISM.core.MatrixArray import MatrixArray
from pyPRISM.core.IdentityMatrixArray import IdentityMatrixArray
from pyPRISM.core.Space import Space
from pyPRISM.core.PairTable import PairTable
from pyPRISM.core.ValueTable import ValueTable
from pyPRISM.core.System import System
from pyPRISM.core.Domain import Domain
from pyPRISM.core.Density import Density
from pyPRISM.core.Diameter import Diameter

from pyPRISM import calculate
from pyPRISM import closure
from pyPRISM import potential
from pyPRISM import omega

from pyPRISM import util

from pyPRISM.version import *





