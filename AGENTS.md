# AGENTS.md - pyPRISM Codebase Guide for LLMs

## Overview

**pyPRISM** is a Python-based, open-source framework for conducting **Polymer Reference Interaction Site Model (PRISM)** theory calculations. PRISM theory describes the equilibrium spatial-correlations of liquid-like polymer systems including melts, blends, solutions, block copolymers, ionomers, liquid crystal forming polymers, and nanocomposites.

### Key Capabilities
- Calculate structural properties (pair correlation functions, structure factors)
- Calculate thermodynamic properties (second virial coefficients, Flory-Huggins interaction parameters, potentials of mean force)
- Solve PRISM equations numerically through a user-friendly scripting interface
- Extend PRISM calculations for coarse-graining atomistic simulation force-fields or modeling experimental scattering data

### Extended Features
This codebase includes additional molecular closures and capabilities:
- R-MPY (Reference Molecular Percus-Yevick)
- R-MMSA (Reference Molecular Mean Spherical Approximation)
- R-LWC (Reference Laria-Wu-Chandler)
- Initial guess calculator based on reference repulsive systems
- Picard iteration solver for PRISM equations

### Current Development Branch
**Branch**: `feat_py3_mol_closures` - Updating molecular closures to Python 3 and modernizing the build system.

---

## CRITICAL SETUP INFORMATION

### Virtual Environment
**⚠️ IMPORTANT**: Before running any Python code or commands in this project, you MUST activate the virtual environment located in the root directory:

```bash
source .venv/bin/activate
```

All Python commands, tests, and scripts should be run within this activated virtual environment.

### Python Version Requirements
- Requires Python ≥ 3.9
- Tested on Python 3.9, 3.10, 3.11, 3.12, 3.13

### Core Dependencies
```
numpy >= 1.8.0
scipy
pint  # For unit conversion
```

### Development Dependencies
```
pytest              # Testing framework
sphinx              # Documentation
sphinx-autobuild    # Live documentation preview
sphinx_rtd_theme    # ReadTheDocs theme
nbsphinx            # Jupyter notebook integration
cython              # For trajectory.Debyer compilation
```

---

## Project Structure

```
/Users/tbm/software/pyPRISM/
├── .venv/                      # ⚠️ Virtual environment - MUST BE SOURCED
├── pyPRISM/                    # Main package (85 Python files)
│   ├── __init__.py             # Package initialization
│   ├── version.py              # Auto-generated version from git tags
│   ├── core/                   # Core PRISM calculation machinery
│   │   ├── System.py           # Primary system definition class
│   │   ├── PRISM.py            # Main PRISM calculation container
│   │   ├── Domain.py           # Space discretization and transforms
│   │   ├── MatrixArray.py      # 3D array container (n×n at each grid point)
│   │   ├── PairTable.py        # Container for pair-wise data
│   │   ├── ValueTable.py       # Container for single-value data
│   │   ├── Density.py          # Density data structure
│   │   ├── Diameter.py         # Diameter data structure
│   │   └── Space.py            # Space enumeration (Real/Fourier)
│   ├── closure/                # Closure relations (14 files)
│   │   ├── Closure.py          # Base class
│   │   ├── AtomicClosure.py    # Base for atomic closures
│   │   ├── MolecularClosure.py # Base for molecular closures
│   │   ├── PercusYevick.py     # PY closure
│   │   ├── HyperNettedChain.py # HNC closure
│   │   ├── MeanSphericalApproximation.py  # MSA closure
│   │   ├── MartynovSarkisov.py # MS closure
│   │   ├── ReferenceMolecularPercusYevick.py  # R-MPY (Python 3 update in progress)
│   │   ├── ReferenceMolecularMeanSphericalApproximation.py  # R-MMSA (Python 3 update)
│   │   └── ReferenceLariaWuChandler.py  # R-LWC (Python 3 update in progress)
│   ├── potential/              # Pair potentials (6 files)
│   │   ├── Potential.py        # Base class
│   │   ├── HardSphere.py
│   │   ├── Exponential.py
│   │   ├── LennardJones.py
│   │   ├── HardCoreLennardJones.py
│   │   └── WeeksChandlerAndersen.py
│   ├── omega/                  # Intra-molecular correlations (13 files)
│   │   ├── Omega.py            # Base class
│   │   ├── SingleSite.py
│   │   ├── NoIntra.py
│   │   ├── InterMolecular.py
│   │   ├── Gaussian.py
│   │   ├── GaussianRing.py
│   │   ├── FreelyJointedChain.py
│   │   ├── NonOverlappingFreelyJointedChain.py
│   │   ├── DiscreteKoyama.py
│   │   ├── FromArray.py        # Load from numpy array
│   │   └── FromFile.py         # Load from file
│   ├── calculate/              # Property calculations (10 files)
│   │   ├── pair_correlation.py
│   │   ├── structure_factor.py
│   │   ├── second_virial.py
│   │   ├── chi.py              # Flory-Huggins parameters
│   │   ├── pmf.py              # Potential of mean force
│   │   ├── solvation_potential.py
│   │   ├── spinodal_condition.py
│   │   ├── initial_guess.py    # Initial guess from reference system
│   │   ├── refDirectCorr.py
│   │   └── refTotalCorr.py
│   ├── trajectory/             # Simulation trajectory utilities
│   │   └── Debyer.pyx          # Cython module for Debye summation
│   ├── util/                   # Utilities
│   │   └── UnitConverter.py    # Unit conversion using pint
│   └── test/                   # Test suite (30 test files)
│       ├── *_test.py           # Unit tests
│       └── data/               # Test data files
├── docs/                       # Sphinx documentation (52 .rst files)
│   ├── conf.py                 # Sphinx configuration
│   ├── index.rst               # Documentation home
│   ├── api/                    # API documentation (auto-generated)
│   ├── install/                # Installation guides
│   ├── Makefile                # Documentation build file
│   └── *.rst                   # Various documentation files
├── tutorial/                   # Jupyter notebook tutorials
│   ├── NB0.*.ipynb             # Introduction
│   ├── NB1.*.ipynb             # Python basics
│   ├── NB2.*.ipynb             # Theory - General liquid theory
│   ├── NB3.*.ipynb             # Theory - PRISM formalism
│   ├── NB4.*.ipynb             # pyPRISM overview
│   ├── NB5.*.ipynb             # Case study - Polymer melts
│   ├── NB6.*.ipynb             # Case study - Nanocomposites
│   ├── NB7.*.ipynb             # Case study - Copolymers
│   ├── NB8.*.ipynb             # pyPRISM internals
│   ├── NB9.*.ipynb             # Advanced topics
│   └── img/                    # Tutorial images
├── data/                       # Reference/example data
├── dev/                        # Development utilities
│   └── zhihao_compare/         # Comparison scripts
├── env/                        # Environment configuration files
├── pyproject.toml              # Modern build configuration (PEP 517/518)
├── setup.py                    # Legacy build configuration
├── requirements.txt            # Dependency list
├── README.md                   # Project overview
├── CONTRIBUTING.md             # Contribution guidelines
├── DEV.md                      # Development/release procedures
├── LICENSE                     # NIST public domain license
└── .travis.yml                 # CI configuration
```

---

## Core Architecture

### Data Flow: Typical PRISM Calculation

```
1. Define System (System.py)
   ↓
2. Set site types, densities, diameters
   ↓
3. Configure interaction potentials (PairTable)
   ↓
4. Assign closures for each site pair
   ↓
5. Define intra-molecular correlations (omega)
   ↓
6. Specify domain (grid discretization)
   ↓
7. Create PRISM object
   ↓
8. Solve PRISM equations (scipy.optimize.root)
   ↓
9. Calculate properties (calculate module)
```

### Key Design Patterns

#### 1. Type-Based Data Keying
All data structures use site types as keys with automatic symmetry handling for unlike pairs:
```python
sys.potential['polymer','particle'] = pyPRISM.potential.Exponential(...)
# Automatically handles symmetry: ['particle','polymer'] returns same
```

#### 2. Space Awareness
`MatrixArray` tracks whether data is in Real or Fourier space, preventing improper operations.

#### 3. Modular Extensibility
Easy to add new components by inheriting from base classes:
- New closures → inherit from `Closure`
- New potentials → inherit from `Potential`
- New omega functions → inherit from `Omega`

#### 4. Hybrid Python/Cython
Performance-critical trajectory analysis uses Cython (`Debyer.pyx`) for speed.

---

## Core Modules in Detail

### pyPRISM.core - Foundation Layer

#### System.py
Primary class for defining complete PRISM systems.
- Holds: site types, densities, diameters, potentials, closures, omega functions, domain
- Main method: `solve()` creates and solves PRISM object
- Type-safe data access via `PairTable` and `ValueTable`

#### PRISM.py
Main container for PRISM calculations.
- Stores: direct correlation (c, C), pair correlation (g, h), total correlation, potential energy
- Key methods:
  - `solve()`: Numerically solves PRISM equations using scipy.optimize.root
  - `cost()`: Cost function for optimization
  - Space transformations between real and Fourier space

#### Domain.py
Discretization and space transformation utilities.
- Defines real and Fourier space grids
- Implements Discrete Sine Transform (DST) for space conversions
- Handles mathematical aspects of radial symmetry

#### MatrixArray.py
3D numpy array container for n×n matrices at each grid point.
- Fundamental data structure for all correlation functions
- Supports numerical and semantic (type-based) indexing
- Tracks space type (Real/Fourier) to prevent invalid operations
- Example: `h['polymer','particle']` returns pair correlation for that interaction

#### PairTable.py & ValueTable.py
Container classes for pair-wise and single-value data.
- Type-keyed access: `table['typeA', 'typeB']`
- Automatic symmetry handling for unlike pairs
- Used for: potentials, closures, densities, diameters

### pyPRISM.closure - Closure Relations

Closure relations bridge the gap between c(r), h(r), and u(r) to solve PRISM equations.

**Atomic Closures** (single-site systems):
- `PercusYevick` (PY): Good for hard-core potentials
- `HyperNettedChain` (HNC): Good for soft potentials
- `MeanSphericalApproximation` (MSA): Approximates directional coupling
- `MartynovSarkisov` (MS): Improved hard-sphere closure

**Molecular Closures** (polymer/multi-site systems):
- `ReferenceMolecularPercusYevick` (R-MPY): Reference-based PY for polymers
- `ReferenceMolecularMeanSphericalApproximation` (R-MMSA): Reference-based MSA
- `ReferenceLariaWuChandler` (R-LWC): Laria-Wu-Chandler closure

⚠️ Molecular closures are currently being updated to Python 3 on the `feat_py3_mol_closures` branch.

### pyPRISM.potential - Interaction Potentials

Pairwise decomposed pair potentials encoding chemical interactions.

Each potential implements `calculate(r)` method:
- `HardSphere`: Simple repulsive (r > σ → U=0, r ≤ σ → U=∞)
- `Exponential`: Exponential decay
- `LennardJones`: Classic 12-6 potential
- `HardCoreLennardJones`: LJ with hard-core repulsion
- `WeeksChandlerAndersen`: Shifted LJ (purely repulsive)

### pyPRISM.omega - Intra-molecular Correlations

Intra-molecular correlation functions encoding polymer structure.

**Analytical Models**:
- `SingleSite`: Isolated particle (Dirac delta)
- `Gaussian`: Gaussian polymer chain
- `GaussianRing`: Gaussian ring polymer
- `FreelyJointedChain` (FJC): Ideal chain (constant bonds, no directional correlation)
- `NonOverlappingFreelyJointedChain` (NFJC): FJC with excluded volume
- `DiscreteKoyama`: Discrete Koyama chain model

**Data Import**:
- `FromArray`: Load from numpy array
- `FromFile`: Load from external file
- `Debyer` (trajectory module): Calculate from molecular dynamics trajectories

### pyPRISM.calculate - Property Calculations

Post-processing functions to extract properties from solved PRISM objects:

**Structural Properties**:
- `pair_correlation()`: Calculate g(r) from h(r)
- `structure_factor()`: Calculate S(k)

**Thermodynamic Properties**:
- `second_virial()`: Calculate B₂
- `chi()`: Calculate Flory-Huggins χ parameters
- `pmf()`: Calculate potential of mean force
- `solvation_potential()`: Calculate solvation free energy
- `spinodal_condition()`: Determine phase separation

**Solver Utilities**:
- `initial_guess()`: Calculate initial guess from reference system
- `refDirectCorr()`: Reference direct correlation
- `refTotalCorr()`: Reference total correlation

---

## Build System

### Modern Build (Primary)
**File**: `pyproject.toml` (PEP 517/518 compliant)
- Build backend: `hatchling`
- Version management: `hatch-vcs` (reads from git tags with pattern `v*.*.*`)
- Auto-generates `pyPRISM/version.py` from git tags

### Legacy Build (Fallback)
**File**: `setup.py`
- Uses `setuptools`
- Handles Cython compilation for `trajectory.Debyer`
- Platform-specific compilation flags

### Building from Source

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Install in development mode
pip install -e .

# With development dependencies
pip install -e ".[dev]"

# With documentation dependencies
pip install -e ".[docs]"

# Compile Cython extensions
python setup.py build_ext --inplace
```

---

## Testing

### Test Framework
`pytest` is used for all unit tests.

### Running Tests

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Run all tests
pytest --verbose

# Run specific test file
pytest pyPRISM/test/Domain_test.py

# Run from Python
import pyPRISM
pyPRISM.test()  # Uses pytest internally
```

### Test Structure
**Location**: `pyPRISM/test/` (30 test files)

Tests cover:
- Core data structures (MatrixArray, PairTable, Domain, etc.)
- Closures (PY, HNC, MSA, MS)
- Potentials (HardSphere, LennardJones, etc.)
- Omega functions (FJC, Gaussian, SingleSite, etc.)
- System and PRISM calculation pipeline

**Test Data**: Reference data in `pyPRISM/test/data/`

---

## Documentation

### Building Documentation

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Install documentation dependencies
pip install -e ".[docs]"

# Build documentation
cd docs
make clean html

# Documentation will be in docs/_build/html/
# Open docs/_build/html/index.html in browser
```

### Documentation Structure

**API Documentation** (`docs/api/`):
- Auto-generated from docstrings using Sphinx autodoc
- Covers all public modules hierarchically

**Tutorials** (`tutorial/`):
- 10 comprehensive Jupyter notebooks (NB0-NB9)
- Cover theory, usage, case studies, internals, advanced topics

**Online Documentation**:
- Hosted at: http://pyPRISM.readthedocs.io
- Auto-builds from master branch

### Docstring Style
Uses **NumPy docstring format** with LaTeX math for equations:

```python
def example_function(param1, param2):
    """
    Brief description.

    Longer description with math: :math:`g(r) = h(r) + 1`

    Parameters
    ----------
    param1 : float
        Description of param1
    param2 : str
        Description of param2

    Returns
    -------
    result : ndarray
        Description of return value

    Notes
    -----
    Additional mathematical details with LaTeX.

    References
    ----------
    .. [1] Citation information
    """
```

---

## Git Workflow

### Current Branch Status
```
Branch: feat_py3_mol_closures
Main Branch: master

Modified Files:
M pyPRISM/closure/ReferenceLariaWuChandler.py
M pyPRISM/closure/ReferenceMolecularMeanSphericalApproximation.py
M pyPRISM/closure/ReferenceMolecularPercusYevick.py

Recent Commits:
- 59cee11: Update to py3 and modern build system
- 317db7e: Update project configuration and dependencies
- 71a19d3: Added differences compared to usnistgov/pyPRISM
```

### Working with Git

```bash
# Check status
git status

# Stage changes
git add <file>

# Commit changes
git commit -m "Descriptive message"

# Push to remote
git push origin feat_py3_mol_closures

# Create pull request to master when ready
```

---

## Common Development Tasks

### 1. Adding a New Closure

```python
# Create new file: pyPRISM/closure/NewClosure.py
from pyPRISM.closure.Closure import Closure

class NewClosure(Closure):
    """
    Description of new closure.

    Mathematical formulation...
    """
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2

    def __call__(self, r, u):
        """Calculate closure relation."""
        # Implement closure equation
        pass

# Add import to pyPRISM/closure/__init__.py
# Write tests in pyPRISM/test/NewClosure_test.py
# Add documentation in docs/api/closure/NewClosure.rst
```

### 2. Adding a New Potential

```python
# Create new file: pyPRISM/potential/NewPotential.py
from pyPRISM.potential.Potential import Potential

class NewPotential(Potential):
    """
    Description of new potential.

    Mathematical formulation...
    """
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2

    def calculate(self, r):
        """Calculate potential at positions r."""
        # Implement potential function
        pass

# Add import to pyPRISM/potential/__init__.py
# Write tests in pyPRISM/test/NewPotential_test.py
# Add documentation in docs/api/potential/NewPotential.rst
```

### 3. Adding a New Property Calculation

```python
# Create new file: pyPRISM/calculate/new_property.py
import numpy as np

def new_property(PRISM, **kwargs):
    """
    Calculate new property from solved PRISM object.

    Parameters
    ----------
    PRISM : pyPRISM.core.PRISM
        Solved PRISM object
    **kwargs
        Additional parameters

    Returns
    -------
    result : float or ndarray
        Calculated property
    """
    # Implementation
    pass

# Add import to pyPRISM/calculate/__init__.py
# Write tests in pyPRISM/test/new_property_test.py
# Add documentation in docs/api/calculate/new_property.rst
```

### 4. Running Example Calculations

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Run comparison script
cd dev/zhihao_compare
python compare.py

# Or launch Jupyter for tutorials
jupyter notebook ../../tutorial/
```

---

## Important Conventions

### Code Style
- Follow PEP 8 for Python code style
- Use descriptive variable names reflecting physical quantities
- Document all public APIs with NumPy-style docstrings
- Include mathematical formulations in docstrings using LaTeX

### Physical Units
- Default units are typically reduced units (kT, σ)
- Use `pyPRISM.util.UnitConverter` for unit conversions
- Document units clearly in docstrings

### Mathematical Conventions
- `r`: Real space position
- `k`: Fourier space wavevector
- `g(r)`: Pair correlation function (radial distribution function)
- `h(r)`: Total correlation function, h(r) = g(r) - 1
- `c(r)`: Direct correlation function
- `u(r)`: Pair potential
- `ω(r)`: Intra-molecular correlation function
- Capital letters (C, H) often denote Fourier-space quantities

### Type Naming
- Use descriptive type names: 'polymer', 'particle', 'solvent', etc.
- Avoid single-letter names unless in mathematical context

---

## Troubleshooting

### Issue: Import errors or module not found
**Solution**: Ensure virtual environment is activated:
```bash
source .venv/bin/activate
```

### Issue: Cython compilation errors
**Solution**: Rebuild Cython extensions:
```bash
python setup.py build_ext --inplace
```

### Issue: Version import errors
**Solution**: Ensure git tags are present or manually create version.py:
```bash
# Check git tags
git tag

# Or manually create version.py
echo '__version__ = "dev"\nversion = "dev"' > pyPRISM/version.py
```

### Issue: Test failures
**Solution**: Check if tests run in isolated environment:
```bash
pytest --verbose -k specific_test_name
```

### Issue: PRISM equations won't converge
**Solutions**:
- Try different closure approximation
- Adjust domain parameters (dr, length)
- Check if potentials are reasonable
- Use better initial guess
- Consult `docs/convergence.rst` for detailed troubleshooting

---

## References and Citations

### Primary Citation
If you use pyPRISM, please cite:

Martin, T.B.; Gartner, T.E III; Jones, R.L.; Snyder, C.R.; Jayaraman, A.
*pyPRISM: A Computational Tool for Liquid State Theory Calculations of Macromolecular Materials*
Macromolecules, 2018, 51 (8), p2906-2922
https://dx.doi.org/10.1021/acs.macromol.8b00011

### Theory Reference
Schweizer, K.S.; Curro, J.G.
*Integral Equation Theory of the Structure of Polymer Melts*
Physical Review Letters, 1987, 58 (3) p246-249
https://doi.org/10.1103/PhysRevLett.58.246

---

## Contact and Support

- **Documentation**: http://pyPRISM.readthedocs.io
- **Issues**: https://github.com/usnistgov/pyPRISM/issues
- **Repository**: https://github.com/usnistgov/pyPRISM

---

## License

This software is in the **public domain** under NIST licensing. See LICENSE file for full details.

NIST Disclaimer: This software is provided 'as is' without warranty. See README.md for full legal disclaimer.

---

## Quick Reference

### Activate Environment
```bash
source .venv/bin/activate
```

### Run Tests
```bash
pytest --verbose
```

### Build Docs
```bash
cd docs && make clean html
```

### Install in Dev Mode
```bash
pip install -e ".[dev,docs]"
```

### Example Calculation
```python
import pyPRISM

sys = pyPRISM.System(['A','B'], kT=1.0)
sys.domain = pyPRISM.Domain(dr=0.01, length=1024)
sys.density['A'] = 0.9
sys.density['B'] = 0.1
sys.diameter['A'] = 1.0
sys.diameter['B'] = 1.0
sys.omega['A','A'] = pyPRISM.omega.FreelyJointedChain(length=100, l=4.0/3.0)
sys.omega['A','B'] = pyPRISM.omega.InterMolecular()
sys.omega['B','B'] = pyPRISM.omega.SingleSite()
sys.potential['A','A'] = pyPRISM.potential.HardSphere()
sys.potential['A','B'] = pyPRISM.potential.HardSphere()
sys.potential['B','B'] = pyPRISM.potential.HardSphere()
sys.closure['A','A'] = pyPRISM.closure.PercusYevick()
sys.closure['A','B'] = pyPRISM.closure.PercusYevick()
sys.closure['B','B'] = pyPRISM.closure.PercusYevick()

PRISM = sys.solve()
pcf = pyPRISM.calculate.pair_correlation(PRISM)
```

---

**Last Updated**: 2026-01-12 (for feat_py3_mol_closures branch)
