.. _noninstall:

Non-Install 
===========
There are use-cases where it makes sense to not permanently install pyPRISM
onto a workstation or computing cluster. All methods below assume that you have
already satisfied the dependencies described in :ref:`dependencies`

Method 1: Command-Line Level
----------------------------
You can add pyPRISM to your current terminal environment so that all scripts
and notebook servers run in this evironment will be able to access pyPRISM.

.. code-block:: bash

    (Linux/OSX) $ export PYTHONPATH=${PYTHONPATH}:/path/to/pyPRISM/dir

    (Windows) > set PATH=%PATH%;C:\path\to\pyPRISM\dir

.. note::
    
    The path in the above examples should be to the directory **containing**
    pyPRISM. The specified directory should be the one containing ``setup.py`` in
    the repository you downloaded or cloned from GitHub and not the one
    containing __init__.py>.

.. warning::

    This method is entirely non-permanent and must be repeated for each new
    terminal or Jupyter instance that is opened.

Method 2: Script or Notebook-Level
----------------------------------
Alternatively, you can add pyPRISM to each script or notebook at runtime by
placing the following code at the top of your script or notebook.

.. code-block:: python
    
    >>> import sys
    >>> sys.insert(0,'/path/to/pyPRISM/directory/')

.. note::
    
    The path in the above examples should be to the directory **containing**
    pyPRISM. The specified directory should be the one containing ``setup.py`` in
    the repository you downloaded or cloned from GitHub and not the one
    containing __init__.py>.

.. warning::

    This method is entirely non-permanent and must be repeated for each new
    script that is run.
