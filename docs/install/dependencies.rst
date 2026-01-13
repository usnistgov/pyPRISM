.. _dependencies:

Dependencies
============

The following are the tested dependencies needed to use pyPRISM:
    - `Python <http://python.org>`__ 3.11
    - `Numpy <http://numpy.org>`__ >= 1.8.0
    - `Scipy  <http://scipy.org/>`__

These dependencies are required for *optional* features
    - `Cython <http://cython.org>`__ (simulation trajectory analyses)
    - `Pint <https://pint.readthedocs.io/en/latest/>`__ (unit conversion utility)

These additional dependencies are needed to run the tutorials
    - `Jupyter  <http://jupyter.org/>`__
    - `matplotlib  <http://matplotlib.org/>`__
    - `Bokeh  <http://bokeh.pydata.org/>`__
    - `HoloViews  <http://holoviews.org/>`__

These additional dependencies are needed to compile the documentation from source
    - `Sphinx <http://sphinx-doc.org>`__
    - `sphinx-autobuild <https://pypi.python.org/pypi/sphinx-autobuild>`__
    - `sphinx_rtd_theme <https://pypi.python.org/pypi/sphinx_rtd_theme>`__
    - `nbsphinx <https://nbsphinx.readthedocs.io>`__
    - `Pandoc <https://pandoc.org>`__ <= 1.19.2

All of these dependecies can be satisfied by creating a conda environment using
the .yml files in source distribution. Note that we provide multiple
environments for different use-cases (e.g., basic user vs. developer). The
environments can be created using the following command
from root directory of the `repository
<https://github.com/usnistgov/pyprism>`__. The root directory is the directory
with the file `setup.py` in it.

.. code-block:: bash

    $ conda env create -f env/py3.yml

Alternatively, all dependecies can be installed in your current Anaconda environment using

.. code-block:: bash

    $ conda install -c conda-forge numpy scipy cython pint jupyter matplotlib bokeh holoviews 

    
Alternatively, all dependencies can be installed via pip

.. code-block:: bash

    $ pip install numpy scipy cython pint jupyter matplotlib bokeh holoviews

Alternatively, each package can be downloaded and installed manually.
