.. _dependencies:

pyPRISM Depedencies
====================

The following are the tested depedencies needed to use pyPRISM:
    - Python 2.7 or 3.5
    - Numpy >= 1.8.0
    - Scipy
    - Cython

These additional dependencies are needed to run the tutorials
    - jupyter
    - matplotlib
    - bokeh
    - holoviews

These additional depedencies are needed to compile the documentation from source
    - sphinx
    - sphinx-autobuild
    - sphinx_rtd_theme

All of these dependecies can be satisfied by creating a conda environment using
the .yml files in source distribution. Note that we provide multiple
environments for difference use-cases (e.g., Python 2 vs. Python 3, basic user
vs. developer). The environments can be created using

.. code-block:: bash

    $ conda env create -f env/py3.yml

Alternatively, all dependecies can be install in your current Anaconda environment using

.. code-block:: bash

    $ conda install numpy scipy cython jupyter matplotlib bokeh holoviews sphinx sphinx-autobuild sphinx_rtd_theme

    
Alternatively, all dependencies can be installed via pip

.. code-block:: bash

    $ pip install numpy scipy cython jupyter matplotlib bokeh holoviews sphinx sphinx-autobuild sphinx_rtd_theme

Alternatively, each package can be downloaded and installed manually.

