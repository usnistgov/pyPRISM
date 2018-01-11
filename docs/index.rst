.. pyPRISM documentation master file, created by
   sphinx-quickstart on Sun Sep 17 12:32:11 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: ../img/TOC.png
    :align: center


pyPRISM
=======

Polymer reference interaction site model (PRISM) theory describes the
correlations of liquid-like polymer systems including melts, blends, solutions,
and composites. Using PRISM theory, one can calculate thermodynamic (second
virial coefficient,  interaction parameters, potential of mean force) and
structural (pair correlation functions, structure factor) descriptors with
either little to no use of mean-field assumptions. Unlike computationally
expensive molecular dynamics or Monte Carlo simulations, PRISM theory can be
numerically solved in seconds or minutes and does not suffer from finite-size
effects. Here, we present a Python-based, open-source framework for conducting
PRISM theory calculations: pyPRISM aims to simplify PRISM-based studies by
providing a simplified scripting interface for numerically solving the PRISM
equations. pyPRISM also provides data structures that simplify PRISM
calculations which allows it to be extended for use in non-prediction tasks
such as for coarse-graining of atomistic simulation force-fields or the
modeling of experimental scattering data. The goal of providing this framework
is to reduce the barrier to accurately using PRISM theory for experts and
non-experts alike and provide a platform for future PRISM and liquid-state
theory innovations. 

**If you use pyPRISM in your work, you *must* cite both of the following articles**

    1. Martin, T.B.; Gartner, T.E. III;  Jones, R.L.; Snyder, C.R.; Jayaraman,
       A.; pyPRISM: A Computational Tool for Liquid State Theory
       Calculations of Macromolecular Materials (submitted)

    2. Schweizer, K.S.; Curro, J.G.; Integral Equation Theory of the Structure
       of Polymer Melts, Physical Review Letters, 1987, 58 (3) p246-249
       doi:10.1103/PhysRevLett.58.246

Tutorial
--------

- `Jupyter Notebooks <https://github.com/usnistgov/pyPRISM_tutorial>`_
- `Static Website <https://nbviewer.jupyter.org/github/usnistgov/pyPRISM_tutorial/blob/master/NB0.Introduction.ipynb>`_

A companion tutorial  to the documentation can be found on GitHub. This
tutorial can be used interactively in a live Jupyter notebook  or rendered as a
static webpage using the nbviewer feature on the Jupyter website. The benefit
of using a live Jupyter notebook is that users are able to edit and run real
pyPRISM code while the static website provides a rapid and setup-free way to
survey the codebase. 

The tutorial not only teaches users how to use pyPRISM, but also covers the
basics PRISM theory, provides a basic introduction to Python, Jupyter, and some
related theoretical concepts. These non-codebase related topics are not covered
in detail in this documentation. The tutorial also goes over several case
studies from the literature and how pyPRISM can be used to reproduce data from
these studies. 

Contact Us
==========
- Dr. Tyler Martin, NIST, 
    `GitHub <https://github.com/martintb>`_,
    `Webpage <https://www.nist.gov/people/tyler-martin>`_,
    `Scholar <https://scholar.google.com/citations?user=9JmVnIIAAAAJ&hl=en>`_
- Mr. Thomas Gartner, University of Delaware, 
    `GitHub <https://github.com/tgartner>`_,
    `Scholar <https://scholar.google.com/citations?user=lzao5SAAAAAJ&hl=en>`_
- Dr. Ron Jones, NIST, 
    `Webpage <https://www.nist.gov/people/ronald-l-jones>`_,
    `Scholar <https://scholar.google.com/citations?user=TKAtIUIAAAAJ&hl=en>`_
- Dr. Chad Snyder, NIST,
    `Webpage <https://www.nist.gov/people/chad-r-snyder>`_,
    `Scholar <https://scholar.google.com/citations?user=MMV7Bf8AAAAJ&hl=en>`_
- Prof. Arthi Jayaraman, University of Delaware, 
    `Webpage <https://udel.edu/~arthij>`_,
    `Scholar <https://scholar.google.com/citations?user=FST4YmwAAAAJ>`_

Contents
--------
.. toctree::
   :maxdepth: 2

   api/pyPRISM
   install
   quickstart
   faq
   convergence
   contribute

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

