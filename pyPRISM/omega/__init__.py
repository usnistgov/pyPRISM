#!python
'''
In PRISM, the molecular structure of molecules is encoded into
*intra*-molecular correlation functions called :math:`\hat{\omega}(k)`. All
connectivity and *intra*-molecular excluded volume is contained in these
functions. During a PRISM calculation, :math:`\hat{\omega}(k)` are specified as
input and are held fixed during the solution procedure. While this leads to a
decoupling of the *intra*-molecular and *inter*-molecular correlations within a
given PRISM calculation, methods such as self-consistent PRISM offer a route to
mitigating this potential problem. See :ref:`scprism` for more details. 

pyPRISM offers several analytical form factors which are listed below. If you
have an analytical :math:`\hat{\omega}(k)` that is not listed, please consider
filing an `Issue <https://github.com/usnistgov/pyPRISM/issues>`_ on GitHub,
implementing the :math:`\hat{\omega}(k)` and sharing with the community. See
:ref:`contribute` for more details.  

Alternatively, if no analytical form exists, :math:`\hat{\omega}(k)` can be
calculated using a simulation. The :class:`pyPRISM.trajectory.Debyer` class
implements the Debye summation method for calculating :math:`\hat{\omega}(k)`
from simulation. 

Finally, the :class:`~pyPRISM.omega.FromArray` and
:class:`~pyPRISM.omega.FromFile` classes exist for loading
:math:`\hat{\omega}(k)` calculated in memory or from another program.
'''
from pyPRISM.omega.Omega import Omega

from pyPRISM.omega.SingleSite import SingleSite
from pyPRISM.omega.NoIntra import NoIntra
from pyPRISM.omega.InterMolecular import InterMolecular

from pyPRISM.omega.FromFile import FromFile
from pyPRISM.omega.FromArray import FromArray

from pyPRISM.omega.Gaussian import Gaussian
from pyPRISM.omega.GaussianRing import GaussianRing

from pyPRISM.omega.DiscreteKoyama import DiscreteKoyama

from pyPRISM.omega.FreelyJointedChain import FreelyJointedChain
from pyPRISM.omega.FreelyJointedChain import FJC

from pyPRISM.omega.NonOverlappingFreelyJointedChain import NonOverlappingFreelyJointedChain
from pyPRISM.omega.NonOverlappingFreelyJointedChain import NFJC

