Verifying an Install
====================
In order to verify your installation and to help ensure that bugs haven't been
introduced, it is useful to run the test suite that is packaged in pyPRISM. If
everything is installed correctly, the test suite should run and successfully
complete all tests. Note that you must have all dependencies satisfied (e.g.
via Ananconda) along with pyPRISM before running the test suite.

.. code-block:: bash

    $ cd <pyPRISM base directory>/pyPRISM/test

    $ python -m pytest --verbose

If the above command throws an error about "No module named pytest", then you
must install the pytest package. This can be done via `Anaconda
<https://www.anaconda.com/download/>`__ or `pip
<https://pypi.python.org/pypi/pip>`__ .

.. code-block:: bash

    $ conda install pytest

or

.. code-block:: bash

    $ pip install pytest




