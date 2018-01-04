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
           Calculations of Macromolecular Materials (to be submitted)

    2. Schweizer, K.S.; Curro, J.G.; Integral Equation Theory of the Structure
           of Polymer Melts, Physical Review Letters, 1987, 58 (3) p246-249
           doi:10.1103/PhysRevLett.58.246

Tutorial
--------

A companion `tutorial <https://github.com/usnistgov/pyPRISM_tutorial>`_ to the
documentation can be found on GitHub. This tutorial can be used interactively
in a live `Jupyter notebook <https://jupyter.org>`_ or rendered as a `static
webpage
<https://nbviewer.jupyter.org/github/usnistgov/pyPRISM_tutorial/blob/master/NB0.Introduction.ipynb>`_
using the nbviewer feature on the Jupyter website. The benefit of using a live
Jupyter notebook is that users are able to edit and run real pyPRISM code while
the static website provide a rapid and setup-free way to survey the codebase. 

The tutorial not only teaches users how to use pyPRISM, but also covers the
basics PRISM theory, provide a basic introduction to Python, Jupyter, and some
related theoretical concepts. These non-codebase related topics are not covered
in detail in this documentation. The tutorial also goes over several case
studies from the literature and how pyPRISM can be used to reproduce data from
these studies. 

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
