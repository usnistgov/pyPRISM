import warnings

try:
    from pyPRISM.trajectory.Debyer import Debyer
except ImportError:
    warnings.warn('Skipping import of Debyer. Module must be compiled with Cython to use. If Cython is in your environment during installation, this should happen automatically ')
