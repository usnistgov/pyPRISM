.. typyPRISM documentation master file, created by
   sphinx-quickstart on Sun Sep 17 12:32:11 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

typyPRISM
=========

Polymer reference interaction site model (PRISM) theory describes the correlations of liquid-like polymer systems including melts, blends, solutions, and composites. Using PRISM theory, one can calculate thermodynamic (second virial coefficient,  interaction parameters, potential of mean force) and structural (pair correlation functions, structure factor) descriptors with either little to no use of mean-field assumptions. Unlike computationally expensive molecular dynamics or Monte Carlo simulations, PRISM theory can be numerically solved in seconds or minutes and doesn’t suffer from finite-size effects. Here, we present a Python-based, open-source framework for conducting PRISM theory calculations: typyPRISM aims to simplify PRISM-based studies by providing a simplified scripting interface for numerically solving the PRISM equations. typyPRISM also provides data structures that simplify PRISM calculations which allows it to be extended for use in non-prediction tasks such as for coarse-graining of atomistic simulation force-fields or the modeling of experimental scattering data. The goal of providing this framework is to reduce the barrier to accurately using PRISM theory for experts and non-experts alike and provide a platform for future PRISM and liquid-state theory innovations. 

**If you use typyPRISM in your work, you *must* cite both of the following articles**

    1. Martin, T.B.; Gartner, T.E. III;  Jones, R.L.; Snyder, C.R.; Jayaraman, A.; typyPRISM: A Computational Tool for Polymer Liquid State Theory Calculations (to be submitted)

    2. Schweizer, K.S.; Curro, J.G.; Integral Equation Theory of the Structure of Polymer Melts, Physical Review Letters, 1987, 58 (3) p246-249 doi:10.1103/PhysRevLett.58.246

Contents
========
.. toctree::
   :maxdepth: 2

   api/typyPRISM
   install
   philosophy
   data_structures
   examples 
   convergence
   faq
   contributing 
