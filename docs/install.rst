.. _install:

Installation Instructions
*************************

.. contents::
    :depth: 2
    

.. _quick_install:

Quick Install
=============
Install pyPRISM with all basic dependences via conda or pip. These commands
should be platform agnostic and work for Unix, OSX, and Windows *if* you have
Anaconda or pip correctly installed. 

.. code-block:: bash

    $ conda install pyPRISM

or

.. code-block:: bash

    $ pip install pyPRISM


Manual Install 
==============
If the above commands do not work, then you can install pyPRISM "manually".
Step 1a shows how to rapidly install all of the dependecies via `conda` while
Step 1b lists the depedencies so you can download and install manually. 

Step 1a: Dependencies via Anaconda (Recommended)
------------------------------------------------
The easiest way to get an environment set up installing it using the
``env/py2.yml``  or ``env/py3.yml`` we have provided for a python2 or
python3 based environment. We recommend the python3 version. If you don't
already have it, install `conda <https://www.continuum.io/downloads>`_. Note that
all of the below instructions can be executed via the anaconda-navigator GUI. To
start, we'll make sure you have the latest version of conda.

.. code-block:: bash

    > conda deactivate

    > conda update anaconda 

Now create the ``pyPRISM_py3`` environment by executing the following. Note that these commands assume your terminal is located in the base directory of the pyPRISM repository.:

.. code-block:: bash

   > conda env create -f env/py3.yml

When installation is complete you must activate the environment. 

.. code-block:: bash

   (Windows)   > activate pyPRISM_py3

.. code-block:: bash

   (OSX/Linux) $ source activate pyPRISM_py3

Later, when you are ready to exit the environment after the tutorial, you can
type:

.. code-block:: bash

   (Windows)   > deactivate 

.. code-block:: bash

   (OSX/Linux) $ source deactivate

If for some reason you want to remove the environment entirely, you can do so by
writing:

.. code-block:: bash

   > conda env remove --name pyPRISM_py3

Note that an environment which satisfies the above dependencies must be
**active** every time you wish to use pyPRISM via script or notebook. If you
open a new terminal, you will have to reactivate the conda environment before
running a script or starting jupyter notebook.

Step 1b: Manual Depedencies
---------------------------
The following are the minimum depedencies needed to use pyPRISM:
    - Python 2.6+ or 3.5+
    - Numpy >= 1.8.0
    - Scipy
    - Cython (not currently but likely in future)

These dependencies are needed to run the tutorials
    - jupyter
    - matplotlib
    - bokeh
    - holoviews

These depedencies are needed to compile the documentation from source
    - sphinx
    - sphinx-autobuild
    - sphinx_rtd_theme
    
Assuming pip is set up, all dependencies can be installed at once via

.. code-block:: bash

    $ pip install numpy scipy cython jupyter matplotlib bokeh holoviews sphinx sphinx-autobuild sphinx_rtd_theme

Alternatively, each package can be downloaded and installed manually via

.. code-block:: bash

    $ cd <downloaded package directory>

    $ python setup.py install

Step 2: Install
---------------
After the depdendencies are satisfied and/or the conda environment is created
**and activated**, pyPRISM can be installed to the system by running:

.. code-block:: bash

    $ cd <pyPRISM base directory>

    $ python setup.py install

Non-Install
===========
There are use-cases where it makes sense to not permanently install pyPRISM
onto a workstation or computing cluster. To aid in this process the ``env/add_pyPRISM.sh``
script was created. Assuming that you have already satisfied the above listed
dependencies, you can add pyPRISM to your current environment via 

.. code-block:: bash

    $ source env/add_pyPRISM.sh

Note that this method is only currently supported for Unix and OSX platforms. 

Codebase Usage
==============
Once pyPRISM is installed or placed in your ``PYTHONPATH`` it can be imported
and used in scripts. To use the examples in the associated pyPRISM tutorial
directory (downloaded separately at the
`pyPRISM_tutorial <https://github.com/usnistgov/pyPRISM_tutorial>`_ repository)

.. code-block:: bash

    $ cd <pyPRISM tutorial directory>

    $ jupyter notebook

This should spawn a jupyter notebook tab in your web browser of choice. If the
tab doesn't spawn, check the terminal for a link that can be copied and pasted.

Verification
============
In order to verify your installation and to help ensure that bugs haven't been introduced, it is useful to run the test suite that is packaged in pyPRISM. If everything is installed correctly, the test suite should run and successfully complete all tests. 

.. code-block:: bash

    $ cd <pyPRISM base directory>/pyPRISM/test

    $ python test.py

Documentation
=============
To build the documentation you'll need to satisfy the above dependency list.
Afterwards you can build the documentation via

.. code-block:: bash

    $ cd <pyPRISM base directory>/docs

    $ make clean

    $ make html

Troubleshooting
===============
#. ModuleNotFoundError or ImportError

    This means that your current distribution of python cannot find the
    pyPRISM package. If you run the command below in a terminal, the
    pyPRISM package *must* be found in one of the listed directories.

    .. code-block:: bash

        python -c "from __future__ import print_function; import sys;print(sys.path)"

    If pyPRISM is not listed, there are several reasons why this might have
    occurred:

    - You are not using the same version of python that you installed pyPRISM
      to. This occurs often when using anaconda because there is often a
      "system" python and an "anaconda" python.

    - You have not activated the conda environment to which you installed
      pyPRISM

    If you cannot seem to install pyPRISM or add pyPRISM to your
    environment manually, you can alternatively hack it into your current
    session as follows. Note that this process will have to be repeated each
    time you start a new Python or IPython session.

    .. code-block:: python
        
        >>> import sys
        >>> sys.insert(0,'/path/to/pyPRISM/directory/')

    Note that the directory in the above command should be the one that
    contains `setup.py`. This directory can be located anywhere on your
    machine.


#. Bash Terminal vs. Windows Terminal vs. Python Terminal vs. IPython Terminal 

    There are strong differences between these terminals and what you can do
    with them. You can identify which environment you are in by looking at the
    terminal itself:

    .. code-block:: bash

        (Bash)          $
        (Windows)       >
        (Python)        >>>
        (IPython)       In [1]: 

    The ``Bash`` and ``Windows`` terminals should be used for installing python
    packages, managing environments, and running python scripts (e.g.  :code:`$
    python run.py`). The ``Python`` and ``IPython`` terminals are for
    interactively running and working with Python code and each line of an
    example can be copied and run in these terminals. In general, the
    ``IPython`` terminal is a superior tool to the standard ``Python`` one and
    offers features such as syntax highlighting and code completion. 

#. Other Internal Error

    Please file a bug report on GitHub. Please see :ref:`contribute` for
    instructions on how to do this. 


