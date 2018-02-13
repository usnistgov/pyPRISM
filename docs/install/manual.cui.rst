Manual Command-Line Install
===========================
If the quick-install commands do not work, then you can install pyPRISM
"manually". After downloading the repository from `GitHub
<https://github.com/usnistgov/pyprism/>`__, follow the steps below. 

.. note::

    Unless specified explicitly, the commands below should work for Linux, OSX,
    and Windows. 

.. note::
    
    For windows users, please ensure you are using the Anaconda command prompt.
    This can be found by opening the Start menu and searching for Anaconda. 


Step 1: Dependencies via Anaconda
---------------------------------
The easiest way to get an environment set up is by using the ``env/py2.yml``
or ``env/py3.yml`` we have provided for a python2 or
python3 based environment. We recommend the python3 version. If you don't
already have it, install `conda <https://www.continuum.io/downloads>`_. Note that
all of the below instructions can be executed via the anaconda-navigator GUI. To
start, we'll make sure you have the latest version of conda.

.. code-block:: bash

    > conda deactivate

    > conda update anaconda 

Now create the ``pyPRISM_py3`` environment by executing the following. Note
that these commands assume your terminal is located in the base directory of
the pyPRISM repository.:

.. code-block:: bash

   > conda env create -f env/py3.yml

When installation is complete you must activate the environment. 

.. code-block:: bash

   (Windows)   > activate pyPRISM_py3

.. code-block:: bash

   (OSX/Linux) $ source activate pyPRISM_py3

Later, when you are ready to exit the environment, you can type:

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

See :ref:`dependencies` for more information.


Step 2: Install pyPRISM
-----------------------
After the depdendencies are satisfied and/or the conda environment is created
**and activated**, pyPRISM can be installed to the system by running:

.. code-block:: bash

    $ cd <pyPRISM base directory>

    $ python setup.py install

