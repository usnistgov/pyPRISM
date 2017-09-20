<p align="center">
    <img src='./img/graphic.png' />
</p>
<h1 align="center">typyPRISM</h1>
<p align="center"> <i>This codebase is in early stage development</i></p>
<p>
Polymer reference interaction site model (PRISM) theory describes the correlations of liquid-like polymer systems including melts, blends, solutions, and composites. Using PRISM theory, one can calculate thermodynamic (second virial coefficient,  interaction parameters, potential of mean force) and structural (pair correlation functions, structure factor) descriptors with either little to no use of mean-field assumptions. Unlike computationally expensive molecular dynamics or Monte Carlo simulations, PRISM theory can be numerically solved in seconds or minutes and doesn’t suffer from finite-size effects. Here, we present a Python-based, open-source framework for conducting PRISM theory calculations: typyPRISM aims to simplify PRISM-based studies by providing a simplified scripting interface for numerically solving the PRISM equations. typyPRISM also provides data structures that simplify PRISM calculations which allows it to be extended for use in non-prediction tasks such as for coarse-graining of atomistic simulation force-fields or the modeling of experimental scattering data. The goal of providing this framework is to reduce the barrier to accurately using PRISM theory for experts and non-experts alike and provide a platform for future PRISM and liquid-state theory innovations. 
</p>

<p align="center"> <b>If you use typyPRISM in your work, you <i>must</i> cite both of the following articles</b></p>

1. Martin, T.B.; Jones, R.L.; Snyder, C.R.; Jayaraman, A.; typyPRISM: A Computational Tool for Polymer Liquid State Theory Calculations (to be submitted)

2. Schweizer, K.S.; Curro, J.G.; INTEGRAL EQUATION THEORY OF THE STRUCTURE OF POLYMER MELTS, Physical Review Letters, 1987, 58 (3) p246-249 doi: http://dx.doi.org/10.1103/PhysRevLett.58.246


Example
=======
Below is an example python script where we use typyPRISM to calculate the pair correlation functions for a
nanocomposite (polymer + particle) with attractive polymer-particle interactions. Below the script is a plot
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

sys.closure['polymer','polymer']   = typyPRISM.closure.PercusYevick()
sys.closure['polymer','particle']  = typyPRISM.closure.PercusYevick()
sys.closure['particle','particle'] = typyPRISM.closure.HyperNettedChain()

PRISM = sys.createPRISM()

PRISM.solve()

pcf = pair_correlation(PRISM)
```
<p align="center">
    <img src='./img/plot.png' />
</p>

Documentation
=============
Code documentation can be found [here](https://readthedocs.io/). The most up to
date code documentation can always be found by compiling from source. 

Depedencies
===========
The following are the minimum depedencies needed to use typyPRISM:

    - Python 2.6+ or 3+
    - Numpy >= 1.8.0
    - Scipy
    - Cython (not currently but likely in future)

These dependencies are needed to run the example notebooks documentation
    
    - jupyter
    - matplotlib
    - bokeh
    - holoviews

These depedencies are needed to compile the documentation from source
    
    - sphinx
    - sphinx-autobuild
    - sphinx_rtd_theme


Quick Install
=============
Install typyPRISM with all basic dependences via conda or pip. These commands
should be platform agnostic and work for Unix, OSX, and Windows *if* you have
Anaconda or pip correctly installed.  For full installation instructions please
see the documentation. 

``` bash
$ conda install typyPRISM
```

or

``` bash
$ pip install typyPRISM
```


