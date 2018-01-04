.. _convergence:

Convergence Tips
================
One of the most frustrating parts of working with PRISM numerically is that the
numerical solver is often unable to converge to a solution. This is manifested
as the funk norm reported by the solver either not decreasing or fluctuating.
The difficulty is in discerning why the solver is unable to converge. This can
be related to the users choice of (perhaps unphysical) parameters or a poor
choice of initial guess passed to the solver. Below are some suggestions on
what to do if you cannot converge to a solution.

Give the solver a better initial guess
--------------------------------------
As is universally the case when using numerical methods, the better the
"initial guess" the better the chance of the numerical method succeding in
finding a minima. By default, pyPRISM uses an uninformed or "dumb" guess,
and this is sufficient for many systems. We are currently working on
developing other methods for creating improved "dumb" guesses.

As an alternative to using an uninformed guess, one can also use the
solution from another PRISM calculation as the guess for their current one.
This is generally done by finding a convergable system that is 'nearby' in
phase space and then using the solution of that problem (PRISM.x) as the
'guess' to a new PRISM solution. This process can be iterated to achieve
convergence in regions of phase space that are not directly convergable.
This process is demonstrated in several of the examples in the `pyPRISM
tutorial <https://github.com/usnistgov/pyPRISM_tutorial>`_.

Change the closures used for some or all of your site pairs
-----------------------------------------------------------
Certain closures perform better under certain conditions, e.g., if
attractive vs. repulsive interactions are used or if certain species have
very asymmetric sizes or interaction strengths. Changing closures for some
or all species may help. In the paper accompanying the pyPRISM tool, we
discuss some suggestions for closures based on the system under study.

Consider your location in phase-space
-------------------------------------
Maybe the equations aren't converging because you aren't within the simple
isotropic liquid region of your system. Try varying the interaction
strength, density, composition, etc. Remember, PRISM cannot predict the
structure of the phase separated state and PRISM may not predict the phase
boundary where you think it should be.

Vary your domain spacing and domain size
----------------------------------------
There are numerical and physical reasons why the details of one's solution
domain might affect the ability of the numerical solver to converge. Ensure
that your domain spacing is small enough (in Real-space) to capture the
smallest feature of interest. It is also important that you have enough
points in your domain for the discrete sine transform to be correct. We
recommend choosing a power of 2 that is (at-least) greater than or equal to
length=1024.  Keeping the number of points in your domain to be a power of
two, as this choice improves the stability of the Fourier transform. 

Try a different numerical solver or solution scheme
---------------------------------------------------
While the default numerical solution method that pyPRISM uses is well
tested and is most-often the best-choice for PRISM, there have been cases
where alternative solvers converge to a solution more easily. See the
`Scipy docs
<https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root.html>`_
for more information on available solvers. See the
:func:`pyPRISM.core.PRISM.PRISM.solve` documentation for how to specify the
solver. 



