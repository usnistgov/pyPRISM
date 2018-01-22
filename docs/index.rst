.. pyPRISM documentation master file, created by
   sphinx-quickstart on Sun Sep 17 12:32:11 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: ../img/TOC_600x.png
    :align: center


pyPRISM
=======

Polymer Reference Interaction Site Model (PRISM) theory describes the
equilibrium spatial-correlations of liquid-like polymer systems including
melts, blends, solutions, block copolymers, ionomers, liquid crystal forming
polymers and nanocomposites. Using PRISM theory, one can calculate
thermodynamic (e.g., second virial coefficients, Flory-Huggins :math:`\chi` interaction
parameters, potentials of mean force) and structural (eg., pair correlation
functions, structure factors) information for these macromolecular materials.
pyPRISM is a Python-based, open-source framework for conducting PRISM theory
calculations. This framework aims to simplify PRISM-based studies by providing
a user-friendly scripting interface for setting up and numerically solving the
PRISM equations. pyPRISM also provides data structures, functions, and classes
that streamline PRISM calculations, allowing pyPRISM to be extended for use in
other tasks such as the coarse-graining of atomistic simulation force-fields or
the modeling of experimental scattering data. The goal of this framework is to
reduce the barrier to correctly and appropriately using PRISM theory and to
provide a platform for rapid calculations of the structure and thermodynamics
of polymeric fluids and nanocomposites. 

**If you use pyPRISM in your work, you *must* cite both of the following articles**

    1. Martin, T.B.; Gartner, T.E. III;  Jones, R.L.; Snyder, C.R.; Jayaraman,
       A.; pyPRISM: A Computational Tool for Liquid State Theory
       Calculations of Macromolecular Materials (submitted)

    2. Schweizer, K.S.; Curro, J.G.; Integral Equation Theory of the Structure
       of Polymer Melts, Physical Review Letters, 1987, 58 (3) 246-249
       doi:10.1103/PhysRevLett.58.246
       [`link <https://doi.org/10.1103/PhysRevLett.58.246>`__]


Contents
--------
.. toctree::
   :maxdepth: 2

   api/pyPRISM
   install/install
   quickstart
   tutorial/tutorial
   scprism
   faq
   convergence
   contribute
   contact
   legal


Legal
=====

NIST Disclaimer
---------------
Any identification of commercial or open-source software in this document is
done so purely in order to specify the methodology adequately. Such
identification is not intended to imply recommendation or endorsement by the
National Institute of Standards and Technology, nor is it intended to imply
that the softwares identified are necessarily the best available for the
purpose.

NIST License
------------
This software was developed by employees of the National Institute of Standards
and Technology (NIST), an agency of the Federal Government. Pursuant to title
17 United States Code Section 105, works of NIST employees are not subject to
copyright protection in the United States and are considered to be in the
public domain. Permission to freely use, copy, modify, and distribute this
software and its documentation without fee is hereby granted, provided that
this notice and disclaimer of warranty appears in all copies.  

THE SOFTWARE IS PROVIDED 'AS IS' WITHOUT ANY WARRANTY OF ANY KIND, EITHER
EXPRESSED, IMPLIED, OR STATUTORY, INCLUDING, BUT NOT LIMITED TO, ANY WARRANTY
THAT THE SOFTWARE WILL CONFORM TO SPECIFICATIONS, ANY IMPLIED WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND FREEDOM FROM
INFRINGEMENT, AND ANY WARRANTY THAT THE DOCUMENTATION WILL CONFORM TO THE
SOFTWARE, OR ANY WARRANTY THAT THE SOFTWARE WILL BE ERROR FREE. IN NO EVENT
SHALL NIST BE LIABLE FOR ANY DAMAGES, INCLUDING, BUT NOT LIMITED TO, DIRECT,
INDIRECT, SPECIAL OR CONSEQUENTIAL DAMAGES, ARISING OUT OF, RESULTING FROM, OR
IN ANY WAY CONNECTED WITH THIS SOFTWARE, WHETHER OR NOT BASED UPON WARRANTY,
CONTRACT, TORT, OR OTHERWISE, WHETHER OR NOT INJURY WAS SUSTAINED BY PERSONS OR
PROPERTY OR OTHERWISE, AND WHETHER OR NOT LOSS WAS SUSTAINED FROM, OR AROSE OUT
OF THE RESULTS OF, OR USE OF, THE SOFTWARE OR SERVICES PROVIDED HEREUNDER.

