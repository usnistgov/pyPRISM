#!python
'''
PRISM is often used in conjunction with molecular simulation techniques, such
as when using Self-Consistent PRISM. This module is intended to provide classes for
working with and analyzing molecular simulation trajectories.


See :ref:`scprism` for more information on the method.
'''
import warnings
from sys import platform as _platform


try:
    from pyPRISM.trajectory.Debyer import Debyer
    from pyPRISM.trajectory.Histogrammer import Histogrammer
except ImportError:
    warnings.warn('Cannot import Cython plugins: compiled Cython module not found.')
    '''
    See http://pyprism.readthedocs.io/en/latest/install/cython.plugins.html
    '''
else:
    if not (_platform == "linux" or _platform == "linux2"):
        warnings.warn('Parallelized Debyer is only supported on Linux. Using slower, serial execution.')
        
