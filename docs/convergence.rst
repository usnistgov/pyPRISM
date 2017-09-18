.. _convergence:

Convergence Tips
================
 - What do I do if the solver isn't converging?
     - Vary your domain spacing and domain size
     - Change your closures
     - Consider your location in phase-space
         maybe the equations aren't converging because you aren't within the
         simple isotropic liquid region of your system. Vary the interactions,
         density, etc
         phase separation low-K
     - Give the solver a better initial guess
         This can often be achieved by finding a convergable system that is 
         'nearby' in phase space and then using the solution of that problem
         i.e. PRISM.x as the 'guess' to a new PRISM solution.
     - (advanced) Perhaps try a different numerical solver or solution scheme


