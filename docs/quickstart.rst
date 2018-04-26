.. _quickstart:

Quickstart Guide
================

Setup
-----

**Requirements**

    - pyPRISM 

    - matplotlib

See :ref:`quick_install` or the full install instructions to get pyPRISM and
set up your environment. Note that you'll need `matplotlib
<https://matplotlib.org>`_ for this example as well. After the environment is
set up, the example below can be copied into a file (e.g. test.py) and run from
the command line via

.. code-block:: bash
    
    $ python test.py

Alternatively, the below code can be copied into your IDE (Spyder, PyCharm) or
notebook provider (Jupyter) of choice. 

Features Used
-------------
- :class:`pyPRISM.core.System`
- :class:`pyPRISM.core.Domain`
- :class:`pyPRISM.core.Density`
- :class:`pyPRISM.core.PRISM`
- :class:`pyPRISM.omega.FreelyJointedChain`
- :class:`pyPRISM.omega.InterMolecular`
- :class:`pyPRISM.potential.HardSphere`
- :class:`pyPRISM.potential.Exponential`
- :class:`pyPRISM.closure.PercusYevick`
- :class:`pyPRISM.closure.HyperNettedChain`
- :class:`pyPRISM.calculate.pair_correlation`

Annotated Example
-----------------
.. code-block:: python

    import pyPRISM
    import matplotlib.pyplot as plt
    
    # The system holds all information needed to set up a PRISM problem. We
    # instantiate the system by specifying the site types and thermal energy
    # level (kT, coarse-grained temperature) of the system. 
    sys = pyPRISM.System(['particle','polymer'],kT=1.0)

    # We must discretize Real and Fourier space
    sys.domain = pyPRISM.Domain(dr=0.01,length=4096)
        
    # The composition of the system is desribed via number densities
    sys.density['polymer']  = 0.75
    sys.density['particle'] = 6e-6
    
    # The diameter of each site is specified (in reduced units)
    sys.diameter['polymer']  = 1.0
    sys.diameter['particle'] = 5.0
    
    # The molecular structure is described via intra-molecular correlation
    # functions (i.e. omegas)
    sys.omega['polymer','polymer']   = pyPRISM.omega.FreelyJointedChain(length=100,l=4.0/3.0)
    sys.omega['polymer','particle']  = pyPRISM.omega.NoIntra()
    sys.omega['particle','particle'] = pyPRISM.omega.SingleSite()
    
    # The site-site interactions are specified via classes which are lazily 
    # evaluated during the PRISM-object creation
    sys.potential['polymer','polymer']   = pyPRISM.potential.HardSphere(sigma=1.0)
    sys.potential['polymer','particle']  = pyPRISM.potential.Exponential(sigma=3.0,alpha=0.5,epsilon=1.0)
    sys.potential['particle','particle'] = pyPRISM.potential.HardSphere(sigma=5.0)
    
    # Closure approximations are also specified via classes
    sys.closure['polymer','polymer']   = pyPRISM.closure.PercusYevick()
    sys.closure['polymer','particle']  = pyPRISM.closure.PercusYevick()
    sys.closure['particle','particle'] = pyPRISM.closure.HyperNettedChain()
    
    # The system class has a helper function to automatically transfer and set up
    # a PRISM object. The PRISM object holds all of the correlation function
    # arrays and the cost function which will be numerically minimized to
    # 'solve' the PRISM equations.
    PRISM = sys.createPRISM()
    
    # Call the numerical solver. By default, this is a Newton-Krylov solver. 
    PRISM.solve()
    
    # Calculate the pair-correlation functions.
    rdf = pyPRISM.calculate.pair_correlation(PRISM)

    # Plot the results using matplotlib
    plt.plot(sys.domain.r,rdf['polymer','polymer'],color='red',lw=1.25)
    plt.plot(sys.domain.r,rdf['polymer','particle'],color='green',lw=1.25)
    plt.plot(sys.domain.r,rdf['particle','particle'],color='blue',lw=1.25)
    plt.show()

.. image:: ../img/nanocomposite_rdf.svg
    :align: center
    :width: 500px


Discussion
----------
The above example sets up a PRISM object, runs a PRISM calculation, and plots
the real-space pair correlation functions for a system of freely-jointed 
polymer chains of length :math:`N=100` mixed with spherical hard nanoparticles of 
diameter :math:`D=5d` (i.e., 5 times the monomer site diameter, :math:`d`). 

In addition to the heterogeneity in size scales, this example 
also demonstrates pyPRISM’s ability to handle heterogeneous interaction 
potentials; in this system the hard sphere potential describes pairwise 
interactions for all species, excepting particle-polymer interactions which 
are modeled via an exponential attraction.

All necessary inputs are specified (site types and system temperature, 
domain size and discretization, site densities and diameters, 
intra-molecular correlation functions, interaction potentials, and closures
used for each pair of site types) and then the PRISM calculation is performed.
See Reference [1] for a full discussion of this system.


More Examples
-------------
A detailed tutorial with examples on how to build and run 
PRISM calculations for a variety of systems is shown in the :ref:`tutorial`.
The tutorial includes a general introduction to Python, PRISM, and the pyPRISM
package. It also contains annotated example scripts that were used to create
all of the case-studies in Reference [2].

References
----------

#. Hooper, J.B.; Schweizer, K.S.; Contact Aggregation, Bridging, and Steric
   Stabilization in Dense Polymer Particle Mixtures, Macromolecules 2005, 38,
   8858-8869 [`link <https://doi.org/10.1021/ma060577m>`__]

#. Martin, T.B.; Gartner, T.E. III; Jones, R.L.; Snyder, C.R.; Jayaraman, A.;
   pyPRISM: A Computational Tool for Liquid State Theory Calculations of
   Macromolecular Materials. (submitted)

