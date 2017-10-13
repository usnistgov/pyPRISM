#!python
from __future__ import division,print_function
import numpy as np
from math import exp,sin,cos,sqrt
from scipy.optimize import root

class DK_density_correction():
    '''Calcluates density correction due to intra-molecular site overlaps
    Currently only implemented for the Semi-flexible Koyama-based 
    intra-molecular correlation function

    **Mathematial Definition**


    **Variable Definitions**


    **Description**
        
    
    References
    ----------
        Kevin G. Honnell, John G. Curro, Kenneth S. Schweizer
        Local structure of semiflexible polymer melts
        Macromolecules, 1990, 23 (14), pp 3496–3505
    
    '''
    def __init__(self,sigma,l,length,lp):
        r'''Constructor

        Arguments
        ---------
        sigma: float
            contact distance between these sites (i.e. site diameter)

        l: float
            bond length
            
        length: float
            number of monomers/sites in the chain

        lp: float
            persistence length of chain
        '''
        self.sigma   = sigma
        self.length  = length
        self.l       = l
        self.lp      = lp
        self.cos0    = 1 - sigma*sigma/(2.0 * l * l)
        self.value   = None

        if self.lp<4.0/3.0:
            raise ValueError('DiscreteKoyama does not support persistence lengths < 4.0/3.0.')
        elif self.lp == 4.0/3.0:
            self.epsilon = 0.0
            self.cos1 = 0.5*( self.cos0**(2.0) - 1.0)/(self.cos0 + 1.0)
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
    
    def density_correction_kernel(self,r):
        
        factor1 = np.pi*self.sigma**(3.0)*(1-3.0*r/(2.0*self.sigma)+r**(3.0)/(2.0*self.sigma**3.0))/6.0
        factor2 = np.zeros_like(r) 
        for i in range(1,self.length-1):
            for j in range(i+2,self.length+1):
                n = abs(i - j)
                factor2 += self.omega_alpha_gamma_kernel(r=r,n=n)
        factor3 = 4.0*np.pi*r**2.0

        return factor1*factor2*factor3

    def omega_alpha_gamma_kernel(self,r,n):
        
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
        
        C = sqrt(0.5 * (5 - 3*r4/(r2*r2)))
        B = sqrt(C*r2)
        Asq = r2*(1-C)/6 #taking the square root results in many domain errors

        omega_ag = (1.0/(8*np.pi**(3.0/2.0)*np.sqrt(Asq)*B*r))*(np.exp(-(r-B)**2.0/(4.0*Asq))-np.exp(-(r+B)**2.0/(4.0*Asq)))
        
        return omega_ag
    
    def density_correction(self,npts=1000):
        
        r = np.linspace(0.0001,self.sigma,npts)
        integral = np.trapz(self.density_correction_kernel(r),r)
        delta_N = integral/(self.length*np.pi*self.sigma**3.0/6.0)

        return delta_N
