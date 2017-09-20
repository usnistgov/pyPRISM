.. _quicstart:

Quickstart Guide
================

Setup
-----

**Requirements**

    - typyPRISM 

    - matplotlib

See :ref:`quick_install` or the full install instructions to get typyPRISM and set up your environment. Note that you'll need `matplotlib <https://matplotlib.org>` for this example as well. After the environment is set up, the example below can be copied into a file (e.g. test.py) and run from the command line via

.. code-block:: bash
    
    $ python test.py

Alternatively, the below code can be copied into your IDE (Spyder, PyCharm) or notebook provider (Jupyter) of choice. 

Features Used
-------------
- :class:`typyPRISM.core.System`
- :class:`typyPRISM.core.Domain`
- :class:`typyPRISM.core.Density`
- :class:`typyPRISM.core.PRISM`
- :class:`typyPRISM.omega.FreelyJointedChain`
- :class:`typyPRISM.omega.InterMolecular`
- :class:`typyPRISM.omega.HardSphere`
- :class:`typyPRISM.closure.PercusYevick`
- :class:`typyPRISM.closure.HyperNettedChain`
- :class:`typyPRISM.calculate.pair_correlation`

Annotated Example
-----------------
.. code-block:: python

    import typyPRISM
    import matplotlib.pyplot as plt
    
    # The system holds all information needed to set up a PRISM problem. We
    # instantiate the system by specifying the site types and thermal energy
    # level (kT, coarse-grained temperature) of the system. 
    sys = typyPRISM.System(['particle','polymer'],kT=1.0)

    # We must discretize Real and Fourier space
    sys.domain = typyPRISM.Domain(dr=0.01,length=4096)
        
    # The composition of the system is desribed via number densities
    sys.density['polymer']  = 0.75
    sys.density['particle'] = 6e-6
    
    # The molecular structure is described via intra-molecular correlation
    # functions (i.e. omegas)
    sys.omega['polymer','polymer']   = typyPRISM.omega.FreelyJointedChain(N=100,l=4.0/3.0)
    sys.omega['polymer','particle']  = typyPRISM.omega.InterMolecular()
    sys.omega['particle','particle'] = typyPRISM.omega.SingleSite()
    
    # The site-site interactions are specified via classes which are lazily 
    # evaluated during the PRISM-object creation
    sys.potential['polymer','polymer']   = typyPRISM.potential.HardSphere(sigma=1.0)
    sys.potential['polymer','particle']  = typyPRISM.potential.Exponential(sigma=3.0,alpha=0.5,epsilon=1.0)
    sys.potential['particle','particle'] = typyPRISM.potential.HardSphere(sigma=5.0)
    
    # Closure approximations are also specified via classes
    sys.closure['polymer','polymer']   = typyPRISM.closure.PercusYevick()
    sys.closure['polymer','particle']  = typyPRISM.closure.PercusYevick()
    sys.closure['particle','particle'] = typyPRISM.closure.HyperNettedChain()
    
    # The system class has a helper function to automatically transfer and set up
    # a PRISM object. The PRISM object holds all of the correlation function
    # arrays and the cost function which will be numerically minimized to
    # 'solve' the PRISM equations.
    PRISM = sys.createPRISM()
    
    # Call the numerical solver. By default, this is a Newton-Krylov solver. 
    PRISM.solve()
    
    # Calculate the pair-correlation functions.
    rdf = typyPRISM.calculate.pair_correlation(PRISM)

    # Plot the results
    plt.plot(sys.domain.r,rdf['polymer','polymer'],color='red',lw=1.25)
    plt.plot(sys.domain.r,rdf['polymer','particle'],color='green',lw=1.25)
    plt.plot(sys.domain.r,rdf['particle','particle'],color='blue',lw=1.25)
    plt.show()


Discussion
----------
The above example 

**References**

    1. Hooper, J.B.; Schweizer, K.S.; Contact Aggregation, Bridging, and Steric Stabilization in Dense Polymer Particle Mixtures, Macromolecules 2005, 38, 8858-8869

