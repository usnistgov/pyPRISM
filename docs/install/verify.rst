Verifying an Install
====================
In order to verify your installation and to help ensure that bugs haven't been
introduced, it is useful to run the test suite that is packaged in pyPRISM. If
everything is installed correctly, the test suite should run and successfully
complete all tests. Note that you must have all dependencies satisfied (e.g.
via Ananconda) along with pyPRISM before running the test suite.

.. code-block:: bash

    $ cd <pyPRISM base directory>/test

    $ python -m pytest --verbose

