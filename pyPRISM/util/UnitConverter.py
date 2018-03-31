import warnings
import pint

class UnitConverter(object):
    r'''Unit conversion utility 
    
    **Description**

        pyPRISM operates in a system of reduced units commonly called 'Lennard
        Jones units'. In this unit system, all measures are reported relative
        to characteristic values: length = :math:`d_c`, mass = :math:`m_c`, and
        energy = :math:`e_c`. This class is designed to make some common
        conversions between reduced and real units easier.
        
        See the Theory.General notebook of the :ref:`tutorial` for a more detailed
        discussion of these units and how to work with the UnitConverter utility.

    .. note::

        The methods prefixed with "to" all expect floating point values in
        reduced units and convert to real units. 

    .. warning::

        This class uses the `Pint <https://pint.readthedocs.io>`_ package. While the
        rest of pyPRISM will function without Pint, this class will not be
        available without this dependency installed in the current environment. 

    
    Example
    -------
    .. code-block:: python

        import pyPRISM

        domain = pyPRISM.Domain(length=4096,dr=0.25)

        # create unit converter utility 
        uc = pyPRISM.util.UnitConverter(dc=1.5,dc_unit='nm')

        # convert wavenumber from LJ units to real units 
        # using built-in conversion
        real_k = uc.toInvAngstrom(domain.k)
        real_k_magnitudes = real_k.magnitude

        # convert radius in real units to reduced units
        # manually using pint
        real_radius = 123.5 # angstrom
        reduced_radius = real_radius * uc('angstrom').to('dc').magnitude


    
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

        self.pint = pint.UnitRegistry()

        dString = 'dchar = {} {} = dc'.format(dc,dc_unit)
        mString = 'mchar = {} {} = mc'.format(mc,mc_unit)
        eString = 'echar = {} {} = ec'.format(ec,ec_unit)
        # print('--> Defining reduced unit {}'.format(dString))
        # print('--> Defining reduced unit {}'.format(mString))
        # print('--> Defining reduced unit {}'.format(eString))
        self.pint.define(dString)
        self.pint.define(mString)
        self.pint.define(eString)

        self.d = self.dc = self.pint.Quantity(1,'dc')
        self.m = self.mc = self.pint.Quantity(1,'mc')
        self.e = self.ec = self.pint.Quantity(1,'ec')

    def __repr__(self):
        return '<UnitConverter  dc:{} | mc:{} | ec:{}>'.format(self.dc.to_base_units(),self.mc.to_base_units(),self.ec.to_base_units())
    
    def __call__(self,unit_string):
        '''Convenience method for accessing the pint UnitRegistry'''
        return self.pint(unit_string)

    def toKelvin(self,temperature):
        r'''Convert thermal energy to temperature units in :math:`K`

        Arguments
        ---------
        temperature: float or np.ndarray of floats
            Value of thermal energy (:math:`k_{B}T`) to be converted

        Returns
        -------
        temperature: Pint Quantity
            temperature in :math:`K` as a Pint Quantity. Use the magnitude
            attribute (temperature.magnitude) to obtain the numerical value of
            the temperature as a floating point value.
        '''
        new_value = (temperature*self.e)/self.pint('boltzmann_constant')

        # need to handle both the molar and non-molar characteristic energy
        try:
            return new_value.to('K')
        except pint.errors.DimensionalityError:
            new_value /= self.pint('N_A')
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
            wavenumbers in :math:`AA^{-1}` as a Pint Quantity. Use the
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
        new_value = density/(self.d**3.0)/self.pint('N_A')
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
        new_value = density*4.0/3.0 * self.pint('pi') * (diameter/2.0)**(3.0)
        return new_value*self.pint('unitless')



