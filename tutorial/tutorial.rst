.. _tutorial:

Tutorial
========

A companion tutorial to the documentation can be found in the source of the
pyPRISM package. This tutorial can be used interactively in live Jupyter
notebooks or rendered as a static document. The benefit of using a live Jupyter
notebook is that users are able to edit and run real pyPRISM code while the
static website provides a rapid, and setup-free way to survey the codebase.  On
top of teaching users how to use pyPRISM, the tutorial covers the basics of
Jupyter notebooks, Python, and PRISM theory.The tutorial also goes over several
case studies from the literature and illustrates how pyPRISM can be used to
reproduce results from these studies. 

Interactive Tutorial
--------------------
- Jupyter Notebooks [`link <https://github.com/usnistgov/pyprism/>`__]
    - The tutorial notebooks are packaged in the main codebase repository under
      the *tutorial* directory. See :ref:`usage` for more details on how to use
      these notebooks.

.. |binder| image:: https://mybinder.org/badge.svg 
    :target: https://mybinder.org/v2/gh/usnistgov/pyprism/master?filepath=tutorial

- Binder |binder|
    - Try out the pyPRISM tutorial without installing!

    .. warning::

        Binder is a *free* service that we are taking advantage of to give
        users a zero-effort chance to try pyPRISM. Users should only run the
        tutorial examples and not custom notebooks. Please do not abuse this
        resource. Once a user has decided to use pyPRISM for research or
        teaching, please download and install pyPRISM locally as described in
        the :ref:`install`.


Non-Interactive Tutorial
------------------------
.. toctree::
    :maxdepth: 1

    NB0.Introduction
    NB1.PythonBasics
    NB2.Theory.General
    NB3.Theory.PRISM
    NB4.pyPRISM.Overview
    NB5.CaseStudies.PolymerMelts
    NB6.CaseStudies.Nanocomposites
    NB7.CaseStudies.Copolymers
    NB8.pyPRISM.Internals
    NB9.pyPRISM.Advanced


.. image:: ../img/tracks.svg
    :width: 600px
    :align: center

