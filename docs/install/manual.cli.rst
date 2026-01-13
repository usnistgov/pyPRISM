.. _manual_cli_install:

Manual Command-Line Install
===========================
If the quick-install commands do not work, then you can install pyPRISM
"manually". After downloading the repository from `GitHub
<https://github.com/usnistgov/pyprism/>`__, follow the steps below. 

.. note::

    Unless specified explicitly, the commands below should work for Linux, macOS,
    and Windows. 

.. note::
    
    For windows users, please ensure you are using the Anaconda command prompt.
    This can be found by opening the Start menu and searching for Anaconda. 


Step 1: Dependencies via Anaconda
---------------------------------
The easiest way to get an environment set up is by using the ``env/py3.yml``
environment file we have provided. If you don't already have it, install
`conda <https://www.continuum.io/downloads>`_. Note that all of the below
instructions can be executed via the anaconda-navigator GUI. To start, we'll
make sure you have the latest version of conda.

.. code-block:: bash

    > conda deactivate

    > conda update anaconda 

Now create the ``pyPRISM_py3`` environment by executing the following. Note
that these commands assume your terminal is located in the base directory of
the pyPRISM repository:

.. code-block:: bash

   > conda env create -f env/py3.yml

When installation is complete you must activate the environment. 

.. code-block:: bash

   (Windows)   > activate pyPRISM_py3

.. code-block:: bash

   (macOS/Linux) $ source activate pyPRISM_py3

Later, when you are ready to exit the environment, you can type:

.. code-block:: bash

   (Windows)   > deactivate 

.. code-block:: bash

   (macOS/Linux) $ source deactivate

If for some reason you want to remove the environment entirely, you can do so by
writing:

.. code-block:: bash

   > conda env remove --name pyPRISM_py3

Note that an environment which satisfies the above dependencies must be
**active** every time you wish to use pyPRISM via script or notebook. If you
open a new terminal, you will have to reactivate the conda environment before
running a script or starting jupyter notebook.

See :ref:`dependencies` for more information.


Step 2: Install pyPRISM
-----------------------
After the dependencies are satisfied and/or the conda environment is created
**and activated**, pyPRISM can be installed to the system by running:

.. code-block:: bash

    $ cd <pyPRISM base directory>

    $ pip install .

.. note::

    As of version 2.0, pyPRISM uses a modern build system (``pyproject.toml`` with
    PEP 517/518). Build dependencies like Cython are automatically installed during
    the build process, so you don't need to install them manually first.

Installation with Optional Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can install pyPRISM with optional dependency groups defined in ``pyproject.toml``:

.. code-block:: bash

    # Install with development dependencies (pytest, Cython)
    $ pip install ".[dev]"

    # Install with documentation dependencies (Sphinx, etc.)
    $ pip install ".[docs]"

    # Install with tutorial dependencies (Jupyter, matplotlib, etc.)
    $ pip install ".[tutorials]"

    # Install with all optional dependencies
    $ pip install ".[dev,docs,tutorials]"

Development/Editable Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For development work where you want changes to the source code to immediately
affect the installed package without reinstalling:

.. code-block:: bash

    $ pip install -e ".[dev]"

This installs pyPRISM in "editable" mode and includes development dependencies
like pytest and Cython.

Alternative: Using uv Package Manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For faster installation, you can use the modern `uv <https://github.com/astral-sh/uv>`__ package manager:

.. code-block:: bash

    $ uv pip install .

    # Or with optional dependencies
    $ uv pip install ".[dev,docs,tutorials]"

