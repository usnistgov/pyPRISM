typyPRISM
=========
A python tool for doing liquid-state theory (PRISM) calculations.

This codebase is in very early stage development. 

Environment  Setup
==================

Dependencies
------------
    - Python 2.5+ and 3.x  compatible 
    - Numpy >= 1.8.0
    - Scipy

Option 1: Conda 
----------------
Install the above depedencies manually or via pip.

Option 2: Conda 
----------------
The easiest way to get an environment set up installing it using the 
``environment2.yml``  or ``environment3.yml`` we have provided. If you
don't already have it, install [conda](https://www.continuum.io/downloads),
and then create the ``typyPRISM2``  or ``typyPRISM3`` environment by executing::
```
   > conda env create -f environment.yml
```
When installation is complete you must activate the environment. If you
are on Windows:
```
   > activate typyPRISM3 #or typyPRISM2
```
If you are using OSX/Linux:
```
   $ source activate typyPRISM3 #or typyPRISM2
```

Later, when you are ready to exit the environment after the tutorial, you can type:
```
   > deactivate
```
If for some reason you want to remove the environment entirely, you can do so by writing:

```
   > conda env remove --name typyPRISM3 # or typyPRISM2
```

Installation 
============

After the depdendencies are satisfied and/or the conda environment is created and activated,
typyPRISM can be installed by running:
```
    > python setup.py install
```
