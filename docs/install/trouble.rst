.. _trouble:

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

    See :ref:`noninstall` for details on how to manually add pyPRISM into your
    environment (assuming that the other installation methods are failing).

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


