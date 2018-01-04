import warnings

try:
    import pint
except ImportError:
    warnings.warn('The Pint python library must be installed for the unit\
                   converter utility to be used. The UnitConverter class will not be\
                   available for use.')
else:
    from pyPRISM.util.UnitConverter import UnitConverter
