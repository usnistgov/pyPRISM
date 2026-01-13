.. _dependencies:

Dependencies
============

The following are the tested dependencies needed to use pyPRISM:
    - `Python <http://python.org>`__ >= 3.12
    - `Numpy <http://numpy.org>`__ >= 2.0.0
    - `Scipy  <http://scipy.org/>`__ >= 1.11.0
    - `Pint <https://pint.readthedocs.io/en/latest/>`__ >= 0.20.0 (unit conversion utility)

.. note::

    As of version 2.0, pyPRISM uses a modern build system based on ``pyproject.toml``
    (PEP 517/518). Build dependencies (including Cython >= 3.0.0 for extension
    compilation) are automatically handled during installation and do not need to be
    manually installed.

These additional dependencies are needed to run the tutorials
    - `Jupyter  <http://jupyter.org/>`__
    - `matplotlib  <http://matplotlib.org/>`__
    - `Bokeh  <http://bokeh.pydata.org/>`__
    - `HoloViews  <http://holoviews.org/>`__

These additional dependencies are needed to compile the documentation from source
    - `Sphinx <http://sphinx-doc.org>`__ >= 7.0.0
    - `sphinx-autobuild <https://pypi.python.org/pypi/sphinx-autobuild>`__
    - `sphinx_rtd_theme <https://pypi.python.org/pypi/sphinx_rtd_theme>`__
    - `nbsphinx <https://nbsphinx.readthedocs.io>`__

These additional dependencies are needed for development
    - `pytest <https://pytest.org>`__ >= 7.0.0
    - `Cython <http://cython.org>`__ >= 3.0.0

Optional Dependency Installation
---------------------------------

As of version 2.0, pyPRISM defines optional dependency groups in ``pyproject.toml`` that
can be installed using pip's extras syntax:

.. code-block:: bash

    # Install with development dependencies (pytest, Cython)
    $ pip install "pyPRISM[dev]"

    # Install with documentation dependencies (Sphinx, etc.)
    $ pip install "pyPRISM[docs]"

    # Install with tutorial dependencies (Jupyter, matplotlib, etc.)
    $ pip install "pyPRISM[tutorials]"

    # Install with all optional dependencies
    $ pip install "pyPRISM[dev,docs,tutorials]"

Conda Environment Installation
-------------------------------

All dependencies can be satisfied by creating a conda environment using
the .yml files in the source distribution. The environments can be created using
the following command from the root directory of the
`repository <https://github.com/usnistgov/pyprism>`__:

.. code-block:: bash

    $ conda env create -f env/py3.yml

Alternatively, core dependencies can be installed in your current Anaconda environment:

.. code-block:: bash

    $ conda install -c conda-forge numpy scipy pint

For tutorial dependencies:

.. code-block:: bash

    $ conda install -c conda-forge jupyter matplotlib bokeh holoviews pandas

