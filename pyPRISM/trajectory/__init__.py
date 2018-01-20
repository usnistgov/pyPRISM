import warnings
from sys import platform as _platform


try:
    from pyPRISM.trajectory.Debyer import Debyer
except ImportError:
    warnings.warn('Cannot import Debyer: compiled Cython module not found.')
    '''
    See http://pyprism.readthedocs.io/en/latest/install/cython.plugins.html
    '''
else:
    if not (_platform == "linux" or _platform == "linux2"):
        warnings.warn('Parallelized Debyer is only supported on Linux. Using slower, serial execution.')
        
