.. _faqs:

Frequently Asked Questions
===========================

Can pyPRISM be used outside of Jupyter? 
---------------------------------------
Of course! pyPRISM is a Python module and can be used in any Python
interface assuming that the dependencies are satisfied. The developers
prefer Jupyter as a teaching environment, so the tutorial uses it. All of
the code in the notebooks can be copied to the Python command line or a
script and they should be able to run.
 
Can pyPRISM handle anisotropic systems?
---------------------------------------
The current implementation of PRISM cannot handle anisotropic systems and
will fail to converge or produce erroneous predictions if used for systems
that are aligned. There is an anisotropic PRISM formalism that the
developers are interested in implementing in the future.

How do I set up my specific system?
-----------------------------------
Please make sure you have looked at ALL case studies in the `tutorial
<https://github.com/usnistgov/pyPRISM_tutorial>`_ and at least skimmed
the documentation. We have attempted to provide a number of different
examples and use-cases. If you think there is a deficiency in the
documentation or tutorial, please file a bug report or submit a question
via the `Issues <https://github.com/usnistgov/pyPRISM/issues>`_
interface.

What do I do if the solver isn't converging? 
--------------------------------------------
There are a variety of reasons why the solver might seem "stuck" i.e. the
function norm isn't decreasing. See :ref:`convergence`

What doesn't pyPRISM doesn't have the feature I need?
-----------------------------------------------------
See :ref:`contribute`

How to file a bug report, suggest a feature or ask a question about pyPRISM?
----------------------------------------------------------------------------
GitHub uses an `Issue <https://github.com/usnistgov/pyPRISM/issues>`_ system to track communication between users and developers. The Issues tool has a flexible tagging feature which handles multiple types of posts including questions, feature requests, bug reports, and general discussion. Users should post to the issue system and the developers (or other users!) will respond as soon as they can.
