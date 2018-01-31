#!python
from __future__ import division,print_function
from pyPRISM.omega.Omega import Omega
import numpy as np
from math import exp,sin,cos,sqrt
from scipy.optimize import root

class DiscreteKoyama(Omega):
    r'''Semi-flexible Koyama-based intra-molecular correlation function

    **Mathematial Definition**

    .. math::
    
        \hat{\omega}(k) = \frac{\sin(Bk)}{Bk}\exp(-A^2k^2)

    .. math::
         
         A^2 = \frac{\langle r_{\alpha,\beta}^2 \rangle (1-C)}{6} 
	
    .. math::
         
         B^2 =  C \langle r_{\alpha,\beta}^2 \rangle  
    
    .. math::
         
         C^2 =  \frac{1}{2}\left(5-3\frac{ \langle r_{\alpha,\beta}^4 \rangle}{ \langle r_{\alpha,\beta}^2 \rangle}\right)


    **Variable Definitions**
        
        - :math:`\hat{\omega}(k)` 
            *intra*-molecular correlation function at wavenumber :math:`k`

        - :math:`\langle r_{\alpha,\beta}^2 \rangle`
            second moment of the distance distribution between sites
            :math:`\alpha` and :math:`\beta`. Please see equation (17) of the
            Reference [1] cited below for the mathematical representation.       
 
        - :math:`\langle r_{\alpha,\beta}^4 \rangle`
            fourth moment of the distance distribution between sites
            :math:`\alpha` and :math:`\beta`. Please see equations (18-24) of
            the reference cited below for the mathematical representation.       


    **Description**
        
        The discrete Koyama :math:`\hat{\omega}(k)` was developed to
        represent a wormlike chain with semiflexibility. This scheme
        interpolates between the rigid-rod and the Gaussian chain limits
        to represent a chain with a given persistence length. This 
        form for :math:`\hat{\omega}(k)` has been shown to match the
        structure of molecular dynamics simulations of Kremer-Grest 
        style bead-spring polymer models. 
    
    References
    ----------
    #. Honnell, K.G., J.G. Curro, and K.S. Schweizer, LOCAL-STRUCTURE OF
       SEMIFLEXIBLE POLYMER MELTS. Macromolecules, 1990. 23(14): p. 3496-3505.
       [`link <https://doi.org/10.1021/ma00216a018>`__]


    Example
    -------
    .. code-block:: python

        import pyPRISM
        import numpy as np
        import matplotlib.pyplot as plt

        #calculate Fourier space domain and omega values
        domain = pyPRISM.domain(dr=0.1,length=1000)
        omega  = pyPRISM.omega.DiscreteKoyama(sigma=1.0,l=1.0,length=100,lp=1.43)
        x = domain.k
        y = omega.calculate(x)
        
        #plot the results using matplotlib
        plt.plot(x,y)
        plt.gca().set_xscale("log", nonposx='clip')
        plt.gca().set_yscale("log", nonposy='clip')

        plt.show()
        
        #define a PRISM system and set omega(k) for type A
        sys = pyPRISM.System(['A','B'],kT=1.0)
        sys.domain = pyPRISM.Domain(dr=0.1,length=1024)
        sys.omega['A','A']  = pyPRISM.omega.DiscreteKoyama(sigma=1.0,l=1.0,length=100,lp=1.43)
    
    '''
    def __init__(self,sigma,l,length,lp):
        r'''Constructor

        Arguments
        ---------
        sigma: float
            contact distance between sites (i.e. site diameter)

        l: float
            bond length
            
        length: float
            number of monomers/sites in the chain

        lp: float
            persistence length of chain
        '''
        self.sigma   = sigma
        self.length  = int(length)
        self.l       = l
        self.lp      = lp
        self.cos0    = 1 - sigma*sigma/(2.0 * l * l)
        self.value   = None

        if self.lp<4.0/3.0:
            raise ValueError('DiscreteKoyama does not support persistence lengths < 4.0/3.0.')
        elif self.lp == 4.0/3.0:
            self.epsilon = 0.0
            self.cos1 = 0.5*(self.cos0-1.0)/(self.cos0 + 1.0)
            self.cos2 = (self.cos0**(3.0) + 1)/(3*self.cos0 + 3)
        else:

            self.cos1 = l/lp - 1
            funk = lambda e: self.cos_avg(e) - self.cos1
            result  = root(funk,1.0)

            if result.success != True:
                raise ValueError('DiscreteKoyama initialization failure. Could not solve for bending energy.')

            self.epsilon = result.x
            self.cos2 = self.cos_sq_avg(self.epsilon)
    def cos_avg(self,epsilon):
        '''First moment of bond angle distribution'''
        e = epsilon
        cos0 = self.cos0
        return 1/e  - ( exp(e) + cos0*exp(-e*cos0) )/( exp(e) - exp(-e*cos0) )
    
    def cos_sq_avg(self,epsilon):
        '''Second moment of bond angle distribution'''
        e = epsilon
        cos0 = self.cos0
        cos1 = self.cos_avg(epsilon)
        return (2/e)*cos1 + ( exp(e) - cos0*cos0*exp(-e*cos0) )/( exp(e) - exp(-e*cos0) )
    
    def kernel_base(self,n):
        ''' Calculates the second and fourth moments of the site separate distance distributions

        .. note::

            See Equation 18 in Reference [1] for more details.

        Arguments
        ---------
        n: int
            Integer separation distance along chain.

        '''
        l = self.l
        q = -self.cos1
        p = (3*self.cos2 - 1)/2
        
        D  = n * n * ((1 + q)/(1 - q))**(2.0) 
        D -= n*(1 + (2*q/(1-q)**(3.0)) * (6 + 5*q + 3*q*q) - 4*p/(1-p)*((1 + q)/(1 - q))**(2.0))
        D += 2*q/(1-q)**(4.0) * (4 + 11*q + 12*q*q)
        D -= 4*p/(1-p) * (1 + 8*q/(1-q)**(3.0) + p/(1-p)*((1 + q)/(1 - q))**(2.0))
        D -= q**(n) * 8*q/(1-q)**(3.0) * (n*(1 + 3*q))
        D -= q**(n) * 8*q/(1-q)**(3.0) * ((1 + 2*q + 3*q*q)/(1-q))
        D -= q**(n) * 8*q/(1-q)**(3.0) * (-2*p/(q-p)**(2.0) *(n*(1-q)*(q-p)+2*q*q-q*p-p))
        D -= 6*q**(2*n+2)/(1-q)**(4.0)
        D += p**(n) * (4/(1-p) * (1 + 8*q/(1-q)**(3.0) - ((1+q)/(1-q))**2.0 * (1 - p/(1-p)) ))
        D -= p**(n) * (16*q*q/(1-q)**(3.0) * (1/(q-p)**(2.0))*(q+q*q-2*p))
        D *= 2/3
        
        r2 = n*l*l*((1-self.cos1)/(1+self.cos1) + 2*self.cos1/n * (1-(-self.cos1)**(n))/(1 + self.cos1)**(2.0))
        r4 = r2*r2 + l*l*l*l*D

        return r2,r4
        

    def koyama_kernel_fourier(self,k,n):
        '''Kernel for calculating omega in Fourier-Space

        .. note::

            See Equation 16 in Reference [1] for more details.

        Arguments
        ---------
        k: np.ndarray, float
            array of wavenumber values to calculate :math:`\omega` at

        n: int
            Integer separation distance along chain.
        '''
        r2,r4 = self.kernel_base(n)
        try:
            C = sqrt(0.5 * (5 - 3*r4/(r2*r2)))
            B = sqrt(C*r2)
            Asq = r2*(1-C)/6 #taking the square root results in many domain errors
        except ValueError as e:
            raise ValueError('Bad chain parameters. (Try reducing epsilon)')
            
        return np.sin(B*k)/(B*k) * np.exp(-Asq*k*k)

    def koyama_kernel_real(self,r,n):
        '''Kernel for calculating omega in Real-Space

        .. note::

            See Equation 12 in Reference [1] for more details.

        Arguments
        ---------
        r: np.ndarray, float
            array of real-space positions to calculate :math:`\omega` at

        n: int
            Integer separation distance along chain.
        '''
        r2,r4 = self.kernel_base(n)
        
        try:
            C = sqrt(0.5 * (5 - 3*r4/(r2*r2)))
            B = sqrt(C*r2)
            Asq = r2*(1-C)/6 #taking the square root results in many domain errors
        except ValueError as e:
            raise ValueError('Bad chain parameters. (Try reducing epsilon)')

        omega_ag = (1.0/(8*np.pi**(3.0/2.0)*np.sqrt(Asq)*B*r))*(np.exp(-(r-B)**2.0/(4.0*Asq))-np.exp(-(r+B)**2.0/(4.0*Asq)))
        
        return omega_ag

    def density_correction_kernel(self,r):
        '''Correction for density due to non-physical overlaps

        .. note::

            See Equation 28 in Reference [1] for more details.

        Arguments
        ---------
        r: np.ndarray, float
            array of real-space positions to calculate :math:`\omega` at
        '''
        
        factor1 = np.pi*self.sigma**(3.0)*(1-3.0*r/(2.0*self.sigma)+r**(3.0)/(2.0*self.sigma**3.0))/6.0
        factor2 = np.zeros_like(r) 
        for i in range(1,self.length-1):
            for j in range(i+2,self.length+1):
                n = abs(i - j)
                factor2 += self.koyama_kernel_real(r=r,n=n)
        factor3 = 4.0*np.pi*r**2.0

        return factor1*factor2*factor3

    def density_correction(self,npts=1000):
        '''Correction for density due to non-physical overlaps

        .. note::

            See Equation 28 in Reference [1] for more details.

        Arguments
        ---------
        npts: int
            number of points to use in numerical integral 
        '''
        
        r = np.linspace(0.0001,self.sigma,npts)
        integral = np.trapz(self.density_correction_kernel(r),r)
        delta_N = integral/(self.length*np.pi*self.sigma**3.0/6.0)

        return delta_N

    def __repr__(self):
        return '<Omega: Koyama>'
    
    def calculate(self,k):
        '''Return value of :math:`\hat{\omega}` at supplied :math:`k`

        Arguments
        ---------
        k: np.ndarray, float
            array of wavenumber values to calculate :math:`\omega` at
        
        '''
        self.value = np.zeros_like(k)
        
        for i in range(1,self.length-1):
            for j in range(i+1,self.length):
                n = abs(i - j)
                self.value += self.koyama_kernel_fourier(k=k,n=n)
        self.value *= 2/self.length
        self.value += 1.0
        
        return self.value


