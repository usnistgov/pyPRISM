Non-Install (for Linux/OSX)
============================
There are use-cases where it makes sense to not permanently install pyPRISM
onto a workstation or computing cluster. To aid in this process the ``env/add_pyPRISM.sh``
script was created. Assuming that you have already satisfied the above listed
dependencies, you can add pyPRISM to your current environment via 

.. code-block:: bash

    $ source env/add_pyPRISM.sh

Note that this method is only currently supported for Unix and OSX platforms.
This method is entirely non-permanent and must be repeated for each new
terminal or Jupyter instance that is opened.
