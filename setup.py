from setuptools import setup,Extension,find_packages
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import numpy as np

import update_version
long,short = update_version.get_git_version()
version = short

'''
To compile the cython plugin in the source directory, run this command:
python setup.py build_ext --inplace
'''
ext_modules = [
                Extension('*', 
                          [ 'pyPRISM/trajectory/*.pyx' ],
				          include_dirs=[np.get_include()],
 						  extra_compile_args=['-fopenmp'],
 		     			  extra_link_args=['-fopenmp']
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
