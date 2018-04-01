<p align="center">
    <img src='./tutorial/img/TOC.png' width='500px'/>
</p>
<h1 align="center">pyPRISM</h1>

<p align="center"> 

<a href='https://travis-ci.com/usnistgov/pyPRISM'>
    <img src='https://travis-ci.com/usnistgov/pyPRISM.svg?token=FULcw9eHMtj7oJcV26rG&branch=master' alt='Master Build Status' />
</a>

<a href='https://travis-ci.com/usnistgov/pyPRISM'>
    <img src='https://travis-ci.com/usnistgov/pyPRISM.svg?token=FULcw9eHMtj7oJcV26rG&branch=dev' alt='Dev Build Status' />
</a>

<a href='http://pyprism.readthedocs.io/en/latest/?badge=latest'>
    <img src='http://readthedocs.org/projects/pyprism/badge/?version=latest' alt='Documentation Status' />
</a>

<a href='https://github.com/usnistgov/pyprism'>
    <img src='https://img.shields.io/badge/Release_Version-1.0.0-blue.svg' alt='Release Version' />
</a>

<a href='https://pyPRISM.readthedocs.io/en/latest/tutorial/tutorial.html'>
    <img src='https://img.shields.io/badge/Tutorial--orange.svg' alt='Tutorial' />
</a>


</p>

<p>
Polymer Reference Interaction Site Model (PRISM) theory describes the
equilibrium spatial-correlations of liquid-like polymer systems including
melts, blends, solutions, block copolymers, ionomers, liquid crystal forming
polymers and nanocomposites. Using PRISM theory, one can calculate
thermodynamic (e.g., second virial coefficients, Flory-Huggins interaction
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
</p>

<p align="center"> <b>If you use pyPRISM in your work, we ask that you please cite both of the following articles</b></p>

1. Martin, T.B.; Gartner, T.E III; Jones, R.L.; Snyder, C.R.; Jayaraman, A.;
   pyPRISM: A Computational Tool for Liquid State Theory Calculations of
   Macromolecular Materials [link](https://dx.doi.org/10.1021/acs.macromol.8b00011)

2. Schweizer, K.S.; Curro, J.G.; Integral Equation Theory of the Structure of
   Polymer Melts, Physical Review Letters, 1987, 58 (3) p246-249 [link](https://doi.org/10.1103/PhysRevLett.58.246)


Example
=======
Below is an example python script where we use pyPRISM to calculate the pair
correlation functions for a nanocomposite (polymer + particle) system with
attractive polymer-particle interactions. Below the script is a plot of the
pair correlation functions from this calculation.

```python
import pyPRISM
from pyPRISM.calculate.pair_correlation import pair_correlation

sys = pyPRISM.System(['particle','polymer'],kT=1.0)
sys.domain = pyPRISM.Domain(dr=0.01,length=4096)
    
sys.density['polymer']  = 0.75
sys.density['particle'] = 6e-6

sys.diameter['polymer']  = 1.0
sys.diameter['particle'] = 5.0

sys.omega['polymer','polymer']   = pyPRISM.omega.FreelyJointedChain(length=100,l=4.0/3.0)
sys.omega['polymer','particle']  = pyPRISM.omega.InterMolecular()
sys.omega['particle','particle'] = pyPRISM.omega.SingleSite()

sys.potential['polymer','polymer']   = pyPRISM.potential.HardSphere(sigma=1.0)
sys.potential['polymer','particle']  = pyPRISM.potential.Exponential(sigma=3.0,alpha=0.5,epsilon=1.0)
sys.potential['particle','particle'] = pyPRISM.potential.HardSphere(sigma=5.0)

sys.closure['polymer','polymer']   = pyPRISM.closure.PercusYevick()
sys.closure['polymer','particle']  = pyPRISM.closure.PercusYevick()
sys.closure['particle','particle'] = pyPRISM.closure.HyperNettedChain()

PRISM = sys.createPRISM()

PRISM.solve()

pcf = pyPRISM.calculate.prism.pair_correlation(PRISM)
```
<p align="center">
    <img src='./tutorial/img/nanocomposite_rdf.png' />
</p>

Quick Install
=============
The commands below should install pyPRISM with all basic dependences via conda
or pip. These commands should be platform agnostic and work for Unix, OSX, and
Windows *if* you have Anaconda or pip installed.  For full installation
instructions please see the documentation. 

``` bash
$ conda install -c conda-forge pyPRISM
```

or

``` bash
$ pip install pyPRISM
```
Documentation
=============

- [ReadTheDocs.io](https://pyPRISM.readthedocs.io/)

Code documentation is hosted on ReadTheDocs.io. The most up to
date code documentation can always be found by compiling from source. 

Contact Us
==========
- Dr. Tyler Martin, NIST, 
    [GitHub](https://github.com/martintb),
    [Webpage](https://www.nist.gov/people/tyler-martin),
    [Scholar](https://scholar.google.com/citations?user=9JmVnIIAAAAJ&hl=en)
- Mr. Thomas Gartner, University of Delaware, 
    [GitHub](https://github.com/tgartner),
    [Scholar](https://scholar.google.com/citations?user=lzao5SAAAAAJ&hl=en)
- Dr. Ron Jones, NIST, 
    [Webpage](https://www.nist.gov/people/ronald-l-jones),
    [Scholar](https://scholar.google.com/citations?user=TKAtIUIAAAAJ&hl=en)
- Dr. Chad Snyder, NIST,
    [Webpage](https://www.nist.gov/people/chad-r-snyder),
    [Scholar](https://scholar.google.com/citations?user=MMV7Bf8AAAAJ&hl=en)
- Prof. Arthi Jayaraman, University of Delaware, 
    [Webpage](https://udel.edu/~arthij),
    [Scholar](https://scholar.google.com/citations?user=FST4YmwAAAAJ)

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

