typyPRISM
=========
A python tool for doing liquid-state theory (PRISM) calculations.

This codebase is in very early stage development. 

Dependencies
------------
    Python 3.5+  (@ operator used)
    
    Numpy >=1.8.0
    
    Scipy
    
Setup
=====
This document explains how to get your computer set up for the
tutorial, including how to install the software libraries.

Step 1: Clone this repo
-----------------------

- Any Linux, Mac OS X, or Windows computer with a web browser should work.  We recommend Chrome, but typically also test Firefox and Safari.
- Clone this repository, e.g. using ```git clone https://github.com/martintb/pe_optimization_tutorial.git```
- Open a terminal window inside the repository.


Step 2: Create a conda environment from ``environment.yml``
-----------------------------------------------------------

The easiest way to get an environment set up for the tutorial is
installing it using the ``environment.yml`` we have provided. If you
don't already have it, install [conda](https://www.continuum.io/downloads),
and then create the ``peopt`` environment by executing::
```
   > conda env create -f environment.yml
```
When installation is complete you must activate the environment. If you
are on Windows:
```
   > activate typyPRISM
```
If you are using OSX/Linux:
```
   $ source activate typyPRISM
```

Later, when you are ready to exit the environment after the tutorial, you can type:
```
   > deactivate
```
If for some reason you want to remove the environment entirely, you can do so by writing:

```
   > conda env remove --name typyPRISM
```
