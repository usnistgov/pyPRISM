.. _faqs:

Frequently Asked Questions
===========================

What systems can be studied with PRISM?
---------------------------------------
- polymer melts/blends
- olefinic and non-olefinic polymers
- linear/branched/dendritic/sidechain polymers
- copolymer melts/blends
- polymer solutions
- nanoparticle solutions
- polymer nanocomposites
- liquid crystals (anistropic formalism)
- micelle Solutions
- polyelectrolytes
- rod-like polymers
- flexible polymers
- ionomers
- ionic liquids

What thermodynamic and structural quantities can PRISM calculate?
-----------------------------------------------------------------
- Second virial coefficients, :math:`B_2`
- Flory effective interaction parameters, :math:`\chi^{eff}`
- Potentials of mean force
- Pair correlation functions (i.e. radial distribution functions)
- Partial structure factors
- Spinodal transition temperatures
- Equations of state
- Isothermal compressibilities

For what systems is PRISM theory not applicable for?
----------------------------------------------------
- macrophase-separated systems
- non-isotropic phases
- systems with strong nematic ordering (without anistropic formalism)
- calculating dynamic properties (e.g., diffusion coefficients, rheological properties)

What are the benefits of using PRISM over other simulation or theory methods?
-----------------------------------------------------------------------------
- is orders of magnitude faster
- typically takes seconds to minutes to solve equations
- does not have finite size effects
- does not need to be equilibrated
- is mostly free of incompressibility assumptions

Why can't I import pyPRISM?
---------------------------
See :ref:`trouble`

Can pyPRISM be used outside of Jupyter? 
---------------------------------------
Of course! pyPRISM is a Python module and can be used in any Python
interface assuming that the dependencies are satisfied. The developers
prefer Jupyter as a teaching environment, so the tutorial uses it. All of
the code in the notebooks can be copied to a Python command line script.
 
Can pyPRISM handle anisotropic systems?
---------------------------------------
The current implementation of PRISM cannot handle anisotropic systems and
will fail to converge or produce erroneous predictions if used for systems
that are aligned. There is an anisotropic PRISM formalism that the
developers are interested in implementing in the future.

How do I set up my specific system?
-----------------------------------
Please make sure you have looked at ALL case studies in the :ref:`tutorial` and
at least skimmed this documentation. We have attempted to provide a number of
different examples and use-cases. If you think there is a deficiency in the
documentation or tutorial, please file a bug report or submit a question
via the `Issues <https://github.com/usnistgov/pyPRISM/issues>`_
interface.

What do I do if the solver isn't converging? 
--------------------------------------------
There are a variety of reasons why the solver might seem "stuck", i.e. the
function norm isn't decreasing. See :ref:`convergence`.

What doesn't pyPRISM doesn't have the feature I need?
-----------------------------------------------------
See :ref:`contribute`

How to file a bug report, suggest a feature or ask a question about pyPRISM?
----------------------------------------------------------------------------
GitHub uses an `Issue <https://github.com/usnistgov/pyPRISM/issues>`_ system to
track communication between users and developers. The Issues tool has a
flexible tagging feature which handles multiple types of posts including
questions, feature requests, bug reports, and general discussion. Users should
post to the issue system and the developers (or other users!) will respond as
soon as they can.
