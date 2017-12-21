import warnings
import pint

class UnitConverter(object):
    r'''Unit conversion utility 
    
    **Description**

        pyPRISM operates in a system of reduced units commonly called 'Lennard
        Jones units'. In this unit system, all measures are reported relative
        to characteristic values: length = :math:`d_c, mass = :math:`m_c`, and
        `energy = :math:`e_c. These characeristic values are chosen for a given
        system to simplify the description of the system. For example, for
        mixture of :math:`d_{1}=2.0` nm and :math:`d_{2}=10` nm diameter
        nanoparticles a user might want to set :math:`d_c = 5 nm` so that the
        diameters can be reported to pyPRISM as :math:`d^{*}_{1} = 1 d_c` and
        :math:`d^{*}_{2} = 5 d_c`. To convert from reduced temperature reported
        in units of thermal energy, :math:`T^{*}`, one must use the relation
        :math:`T^{*} = k_{B}T/e_{c}`
        
        
        While understanding these relationships is important, it can be tediuos
        for those outside of the simulation and theory fields to work in these
        unit systems. `UnitConverter` class is designed to allow for easy
        translation between reduced and real unit systems. See the examples
        below.

    .. note::

        The methods prefixed with "to" all expect floating point values in
        reduced units and convert to real units. 

    .. warning::

        This class uses the `Pint <pint.readthedocs.io>`_ package. While the
        rest of pyPRISM will function without Pint, this class will not be
        available without this dependency installed in the current environment. 

    
    
    Example
    -------
    .. code-block:: python

        import pyPRISM

        domain = pyPRISM.Domain(length=4096,dr=0.25)

        uc = pyPRISM.util.UnitConverter(dc=1.5,dc_unit='nm')

        real_k = uc.toInvAngstrom(domain.k)

        real_k_magnitudes = real_k.magnitude

    
    '''
    def __init__(self,
                 dc=1.0,   dc_unit='nanometer',
                 mc=14.02, mc_unit='gram/mole',
                 ec=2.48,  ec_unit='kilojoule/mole'):
        r''' Constructor
        
        Arguments
        ---------
        dc,dc_unit: float,str
            Magnitude and unit of characteristic distance

        mc,mc_unit: float,str
            Magnitude and unit of characteristic mass

        ec,ec_unit: float,str
            Magnitude and unit of characteristic energy


        Attributes
        ----------
        d,dc: Pint Quantity
            The defined characteristic distance as a defined Pint Quantity.

        m,mc: Pint Quantity
            The defined characteristic mass as a defined Pint Quantity.

        e,ec: Pint Quantity
            The defined characteristic energy as a defined Pint Quantity.

        '''

        self.ureg = pint.UnitRegistry()

        dString = 'dchar = {} {} = dc'.format(dc,dc_unit)
        mString = 'mchar = {} {} = mc'.format(mc,mc_unit)
        eString = 'echar = {} {} = ec'.format(ec,ec_unit)
        print('--> Defining reduced unit {}'.format(dString))
        print('--> Defining reduced unit {}'.format(mString))
        print('--> Defining reduced unit {}'.format(eString))
        self.ureg.define(dString)
        self.ureg.define(mString)
        self.ureg.define(eString)

        self.d = self.dc = self.ureg.Quantity(1,'dc')
        self.m = self.mc = self.ureg.Quantity(1,'mc')
        self.e = self.ec = self.ureg.Quantity(1,'ec')
    def toKelvin(self,temperature):
        r'''Convert thermal energy to temperature units in Kelvin

        Arguments
        ---------
        temperature: float or np.ndarray of floats
            Value of thermal energy (:math:`k_{B}T`) to be converted

        Returns
        -------
        temperature: Pint Quantity
            temperature in Kelvin as a Pint Quantity. Use the magnitude
            attribute (temperature.magnitude) to obtain the numerical value of
            the temperature as a floating point value.
        '''
        new_value = (temperature*self.e)/self.ureg('boltzmann_constant')

        # need to handle both the molar and non-molar characteristic energy
        try:
            return new_value.to('K')
        except pint.errors.DimensionalityError:
            new_value /= self.ureg('N_A')
            return new_value.to('K')
    def toCelcius(self,temperature):
        r'''Convert thermal energy to temperature units in Celcius

        Arguments
        ---------
        temperature: float or np.ndarray of floats
            Value of thermal energy (:math:`k_{B}T`) to be converted

        Returns
        -------
        temperature: Pint Quantity
            temperature in Kelvin as a Pint Quantity. Use the magnitude
            attribute (temperature.magnitude) to obtain the numerical value of
            the temperature as a floating point value.
        '''
        return self.toKelvin(temperature).to('C')
    def toInvAngstrom(self,wavenumber):
        r'''Convert wavenumbers to real units

        Arguments
        ---------
        wavenumber: float, or np.ndarray of floats
            Value(s) of wavenumbers to be converted

        Returns
        -------
        wavenumber: Pint Quantity
            wavenumbers in :math:`Ang^{-1}` as a Pint Quantity. Use the
            magnitude attribute (wavenumber.magnitude) to obtain the numerical
            value of the wavenumber as a floating point value.
        '''
        new_value = wavenumber*(1.0/self.d)
        return new_value.to('angstrom^-1')
    def toInvNanometer(self,wavenumber):
        r'''Convert wavenumbers to real units

        Arguments
        ---------
        wavenumber: float, or np.ndarray of floats
            Value(s) of wavenumbers to be converted

        Returns
        -------
        wavenumber: Pint Quantity
            wavenumbers in :math:`nm^{-1}` as a Pint Quantity. Use the
            magnitude attribute (wavenumber.magnitude) to obtain the numerical
            value of the wavenumber as a floating point value.
        '''
        return self.toInvAngstrom(wavenumber).to('nanometer^-1')
    def toConcentration(self,density):
        r'''Convert reduced number density to real concentration units

        Arguments
        ---------
        density: float, or np.ndarray of floats
            Value(s) of density to be converted

        Returns
        -------
        concentration: Pint Quantity
            density in :math:`mol/L` as a Pint Quantity. Use the
            magnitude attribute (concentration.magnitude) to obtain the
            numerical value of the contration as a floating point value.
        '''
        new_value = density/(self.d**3.0)/self.ureg('N_A')
        return new_value.to('mol/L')
    def toVolumeFraction(self,density,diameter):
        r'''Convert reduced number density to volume fraction

        Arguments
        ---------
        density: float, or np.ndarray of floats
            Value(s) of density to be converted

        diameter: float
            diameter of the site associated with the density

        Returns
        -------
        vol_fraction: Pint Quantity
            unitless volume as a Pint Quantity. Use the magnitude attribute
            (vol_fraction.magnitude) to obtain the numerical value of the
            volume fraction as a floating point value.
        '''
        new_value = density*4.0/3.0 * self.ureg('pi') * (diameter/2.0)**(3.0)
        return new_value*ureg('unitless')



