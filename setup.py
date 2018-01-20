from setuptools import setup,Extension,find_packages
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import numpy as np

## Try to use git-describe to get up-to-date version
import update_version
long,short = update_version.get_git_version()
version = short


## Detect os
from sys import platform as _platform

if _platform == "linux" or _platform == "linux2":
    extra_compile_args = ['-fopenmp']
    extra_link_args = ['-fopenmp']
else:
    extra_compile_args = None
    extra_link_args = None

# elif _platform == "darwin":
#           # MAC OS X
# elif _platform == "win32":
#              # Windows
# elif _platform == "win64":
# # Windows 64-bit

'''
To compile the cython plugin in the source directory, run this command:
python setup.py build_ext --inplace
'''
ext_modules = [
                Extension('*', 
                          [ 'pyPRISM/trajectory/*.pyx' ],  
                          include_dirs=[np.get_include()],
                          extra_compile_args=extra_compile_args,
                          extra_link_args=extra_link_args
                          ),
              ]

setup(
    name='pyPRISM',
	ext_modules= cythonize(ext_modules),
    description='A python tool for Polymer Reference Interactions Site Model (PRISM) calculations',
    author='Tyler B. Martin',
    author_email = 'tyler.martin@nist.gov',
    version=version,
    packages=find_packages(where='.'),
    license='LICENSE',
    long_description=open('README.md').read(),
)
