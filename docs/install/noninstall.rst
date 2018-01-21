Non-Install 
===========
There are use-cases where it makes sense to not permanently install pyPRISM
onto a workstation or computing cluster. Assuming that you have already
satisfied the above listed dependencies, you can add pyPRISM to your current
environment via 

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
