.. _convergence:

Convergence Tips
================
 - What do I do if the solver isn't converging?
 	
	- Vary your domain spacing and domain size. 
		Try to keep the number of points in your domain 
		to be a power of two, as this choice improves the 
       	  	stability of the Fourier transform.
     
     	- Change the closures used for some or all of your site pairs.
		Certian closures perform better under certain conditions,
		e.g. if attractive vs. repulsive interactions are used, or
		if certain species have very asymmetric sizes or interaction
		strengths. Changing closures for some or all species may help.     

     	- Consider your location in phase-space.
         	Maybe the equations aren't converging because you aren't within the
         	simple isotropic liquid region of your system. Try varing the 
	 	interaction strength, density, composition, etc.
     
     	- Give the solver a better initial guess.
         	This can often be achieved by finding a convergable system that is 
         	'nearby' in phase space and then using the solution of that problem
         	i.e. PRISM.x as the 'guess' to a new PRISM solution. This process
	 	can be iterated to acheive convergence in regions of phase space that
	 	are not directly convergable. This process is demonstrated in several
	 	of the examples in the
	 	`pyPRISM_tutorial <https://github.com/usnistgov/pyPRISM_tutorial>`_.
     
     	- (advanced) Perhaps try a different numerical solver or solution scheme.


