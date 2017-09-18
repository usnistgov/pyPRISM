Installation Instructions
*************************

.. contents::
    :depth: 2
    

Quick Install
=============
Install typyPRISM with all basic dependences via conda or pip. These commands
should be platform agnostic and work for Unix, OSX, and Windows *if* you have
Anaconda or pip correctly installed. 

.. code-block:: bash

    $ conda install typyPRISM

or

.. code-block:: bash

    $ pip install typyPRISM


Manual Install 
==============

Step 1a: Dependencies via Anaconda (Recommended)
------------------------------------------------
The easiest way to get an environment set up installing it using the
``environment2.yml``  or ``environment3.yml`` we have provided for a python2 or
python3 based environment. We recommend the python3 version. If you don't
already have it, install `conda <https://www.continuum.io/downloads>`_. Note that
all of the below instructions can be executed via the anaconda-navigator GUI. To
start, we'll make sure you have the latest version of conda.

.. code-block:: bash

    > conda deactivate

    > conda update anaconda 

Now create the ``typyPRISM3`` environment by executing:

.. code-block:: bash

   > conda env create -f environment3.yml

When installation is complete you must activate the environment. 

.. code-block:: bash

   (Windows)   > activate typyPRISM3 

.. code-block:: bash

   (OSX/Linux) $ source activate typyPRISM3 

Later, when you are ready to exit the environment after the tutorial, you can
type:

.. code-block:: bash

   (Windows)   > deactivate 

.. code-block:: bash

   (OSX/Linux) $ source deactivate

If for some reason you want to remove the environment entirely, you can do so by
writing:

.. code-block:: bash

   > conda env remove --name typyPRISM3 

Note that an environment which satisfies the above dependencies must be
**active** every time you wish to use typyPRISM via script or notebook. If you
open a new terminal, you will have to reactivate the conda environment before
running a script or starting jupyter notebook.

Step 1b: Depedencies via pip
----------------------------
The following are the minimum depedencies needed to use typyPRISM:
- Python 2.6+ or 3+
- Numpy >= 1.8.0
- Scipy
- Cython (not currently but likely in future)

These dependencies are needed to run the example notebooks documentation
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

    > pip install numpy scipy cython jupyter matplotlib bokeh holoviews sphinx sphinx-autobuild sphinx_rtd_theme

Alternatively, each package can be downloaded and installed manually via

.. code-block:: bash

    > cd <downloaded package directory>

    > python setup.py install

Step 2: Install
---------------
After the depdendencies are satisfied and/or the conda environment is created
and activated, typyPRISM can be installed to the system by running:

.. code-block:: bash

    > cd <typyPRISM base directory>

    > python setup.py install

Non-Install
===========
There are use-cases where it makes sense to not permanently install typyPRISM
onto a workstation or computing cluster. To aid in this process the ``ENV.sh``
script was created. Assuming that you have already satisfied the above listed
dependencies, you can add typyPRISM to your current environment via 

.. code-block:: bash

    $ source ENV.sh

Note that this method is only currently supported for Unix and OSX platforms. 

Codebase Usage
=============
Once typyPRISM is installed or placed in your ``PYTHONPATH`` it can be imported
and used in scripts. To use the examples in source directory

.. code-block:: bash

    > cd <typyPRISM base directory>/examples

    > jupyter notebook

This should spawn a jupyter notebook tab in your web browser of choice. If the
tab doesn't spawn, check the terminal for a link that can be copied and pasted.

Documentation
=============
To build the documentation you'll need to satisfy the above dependency list.
Afterwards you can build the documentation via

.. code-block:: bash

    $ cd <typyPRISM base directory>/docs

    $ make clean

    $ make html
