<p align="center">
    <img src='./img/graphic.png' />
</p>
<h1 align="center">typyPRISM</h1>

Polymer reference interaction site model (PRISM) theory describes the correlations of liquid-like polymer systems including melts, blends, solutions, and composites. PRISM. *typyPRISM* is a Python-based, open-source framework for conducting PRISM theory calculations: typyPRISM aims to simplify PRISM-based studies by providing a simplified scripting interface for numerically solving the PRISM equations. Furthermore, typyPRISM provides data structures that simplify PRISM calculations which allow it to be extended for use in non-prediction tasks such as for coarse-graining of atomistic simulation force-fields or the modeling of experimental scattering data. The goal of providing this framework is to reduce the barrier to using PRISM theory for experts and non-experts alike and provide a platform for future PRISM and liquid-state theory innovations. 

_This codebase is in very early stage development_

**If you use typyPRISM in your work, you must cite both of the following articles**

1. Martin, T.B.; Jones, R.L.; Snyder, C.R.; Jayaraman, A.; typyPRISM: A Computational Tool for Polymer Liquid State Theory Calculations (to be submitted)
2. Schweizer, K.S.; Curro, J.G.; INTEGRAL EQUATION THEORY OF THE STRUCTURE OF POLYMER MELTS, Physical Review Letters, 1987, 58 (3) p246-249 doi: http://dx.doi.org/10.1103/PhysRevLett.58.246


Example
=======
Below is an example python script where we use typyPRISM to calculate the pair correlation functions for a
nanocomposite (polymer + particle) which attractive polymer-particle interactions. Below the script is a plot
of the pair correlation functions from this calculation.

```python
import typyPRISM
from typyPRISM.calculate.prism.pair_correlation import pair_correlation

sys = typyPRISM.System(['particle','polymer'],kT=1.0)
sys.domain = typyPRISM.Domain(dr=0.01,length=4096)
    
sys.density['polymer']  = 0.75
sys.density['particle'] = 6e-6

sys.omega['polymer','polymer']   = typyPRISM.omega.FreelyJointedChain(N=100,l=4.0/3.0)
sys.omega['polymer','particle']  = typyPRISM.omega.NoIntra()
sys.omega['particle','particle'] = typyPRISM.omega.SingleSite()

sys.potential['polymer','polymer']   = typyPRISM.potential.HardSphere(sigma=1.0)
sys.potential['polymer','particle']  = typyPRISM.potential.Exponential(sigma=3.0,alpha=0.5,epsilon=1.0)
sys.potential['particle','particle'] = typyPRISM.potential.HardSphere(sigma=5.0)

sys.closure['polymer','polymer']  = typyPRISM.closure.PercusYevick()
sys.closure['polymer','particle']  = typyPRISM.closure.PercusYevick()
sys.closure['particle','particle'] = typyPRISM.closure.HyperNettedChain()

PRISM = sys.createPRISM()

PRISM.solve()

pcf = pair_correlation(PRISM)
```
![plot of results](img/plot.png)

Installation
============

Dependencies
------------
- Python 2.6+ or 3+
- Numpy >= 1.8.0
    - Need support for linear algebra on stacked arrays
- Scipy
- Cython (not currently but likely in future)

Dependency Option 1: Anaconda 
------------------------------
The easiest way to get an environment set up installing it using the 
``environment2.yml``  or ``environment3.yml`` we have provided for a python2 or
python3 based environment. We recommend the python3 version. If you
don't already have it, install [conda](https://www.continuum.io/downloads),
and then create the `typyPRISM3`` environment by executing::
```
   > conda env create -f environment3.yml
```
When installation is complete you must activate the environment. If you
are on Windows:
```
   > activate typyPRISM3
```
If you are using OSX/Linux:
```
   $ source activate typyPRISM3
```

Later, when you are ready to exit the environment after the tutorial, you can type:
```
   > deactivate
```

If for some reason you want to remove the environment entirely, you can do so by writing:
```
   > conda env remove --name typyPRISM3 
```
Note that an environment which satisfies the above dependencies must be **active** every time
you wish to use typyPRISM. If you open a new terminal, you will have to reactivate the conda
environment before running a script or starting jupyter notebook.

Dependency Option 2: Manual 
---------------------------
Install the above depedencies manually or via pip.

Install
--------
After the depdendencies are satisfied and/or the conda environment is created and activated,
typyPRISM can be installed by running:
```
    > python setup.py install
```
