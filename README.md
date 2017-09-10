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
Please see the [wiki](https://github.com/usnistgov/typyPRISM/wiki) for user-documentation and
frequently asked questions (FAQs). We intend to update this page as new challenges are identified
in using typyPRISM. The wiki also contains a project roadmap and information about how to extend 
typyPRISM and contribute these changes back to this primary repository. 

Code documentation can be found [here](https://readthedocs.io/). The most up to date code documentation 
can always be found by compiling from source. Assuming you have [Sphinx](http://www.sphinx-doc.org/en/stable/) 
installed:
```
    > cd <typyPRISM base directory>/doc
    > make
```

Installation
============

Step 1a: Dependencies via Anaconda (Recommended)
------------------------------------------------
The easiest way to get an environment set up installing it using the 
``environment2.yml``  or ``environment3.yml`` we have provided for a python2 or
python3 based environment. We recommend the python3 version. If you
don't already have it, install [conda](https://www.continuum.io/downloads). Note that
all of the below instructions can be executed via the anaconda-navigator GUI. To start,
we'll make sure you have the latest version of conda.
```
    > conda deactivate
    > conda update anaconda 
```
Now create the ``typyPRISM3`` environment by executing:
```
   > conda env create -f environment3.yml
```
When installation is complete you must activate the environment. 
```
   (Windows)   > activate typyPRISM3 
   (OSX/Linux) $ source activate typyPRISM3 
```

Later, when you are ready to exit the environment after the tutorial, you can type:
```
   (Windows)   > deactivate 
   (OSX/Linux) $ source deactivate
```

If for some reason you want to remove the environment entirely, you can do so by writing:
```
   > conda env remove --name typyPRISM3 
```
Note that an environment which satisfies the above dependencies must be **active** every time
you wish to use typyPRISM via script or notebook. If you open a new terminal, you will have to 
reactivate the conda environment before running a script or starting jupyter notebook.

Step 1b: Depedencies via pip
----------------------------
The following are the minimum depedencies needed to use typyPRISM:
- Python 2.6+ or 3+
- Numpy >= 1.8.0
    - Need support for linear algebra on stacked arrays
- Scipy
- Cython (not currently but likely in future)

These extra dependencies are needed to run the example notebooks:
- jupyter
- matplotlib
- bokeh
- holoviews

Assuming pip is set up, all dependencies can be installed at once via
```
    > pip install numpy scipy cython jupyter matplotlib bokeh holoviews
```

Alternatively, each package can be downloaded and installed manually via
```
    > cd <downloaded package directory>
    > python setup.py install
```
Step 2: Install
---------------
After the depdendencies are satisfied and/or the conda environment is created and activated,
typyPRISM can be installed to the system by running:
```
    > python setup.py install
```
Step 3: Usage
---------------
Once typyPRISM is installed or placed in your ``PYTHONPATH`` it can be imported and used in scripts
as shown in the above example. To use the examples in source directory
```
    > cd <typyPRISM base directory>/examples
    > jupyter notebook
```
This should spawn a jupyter notebook tab in your web browser of choice. If the tab doesn't spawn, check the
terminal for a link that can be copied and pasted.
