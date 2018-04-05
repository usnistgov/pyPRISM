from setuptools import setup,Extension,find_packages

## GET VERSION
import versiontools
version = versiontools.get_python_version()

## HANDLE CYTHON
# Cython needs to be handled with care as PIP cannot know to install cython
# *before* it gets to the setup.py. We handle this by following the suggestion
# here: https://stackoverflow.com/questions/4505747
try:
    from Cython.Distutils import build_ext
    from Cython.Build import cythonize
    import numpy as np
except ImportError:
    # Cython is not installed! Create C-extensions using c-files
    use_cython = False
    print('Using Cython to build extension from pyx!')
else:
    # Cython is installed! Create C-extensions using pyx-files
    use_cython = True
    print('Warning! Building extension from c-files, which may be out-of-date.')


## DETECT OS
# We need to be able handle the idiosyncracies of different OS
from sys import platform as _platform
if _platform == "linux" or _platform == "linux2": #Linux
    extra_compile_args = ['-fopenmp']
    extra_link_args = ['-fopenmp']
elif _platform == "darwin":# MAC OSX
    extra_compile_args = None
    extra_link_args    = None
elif _platform == "win32": # Windows 32-bit
    extra_compile_args = None
    extra_link_args    = None
elif _platform == "win64": # Windows 64-bit
    extra_compile_args = None
    extra_link_args    = None
else: # Catch-All
    extra_compile_args = None
    extra_link_args    = None

## IF CYTHON
cmdclass = {}
ext_modules = []
if use_cython:
    ext_modules += [
                    Extension('pyPRISM.trajectory.Debyer', 
                              [ 'pyPRISM/trajectory/Debyer.pyx' ],  
                              include_dirs=[np.get_include()],
                              extra_compile_args=extra_compile_args,
                              extra_link_args=extra_link_args
                              ),
                   ]
    
    ext_modules = cythonize(ext_modules)
    cmdclass.update({'build_ext':build_ext})
else:
    ext_modules += [
                    Extension('pyPRISM.trajectory.Debyer', 
                              [ 'pyPRISM/trajectory/Debyer.c' ],  
                              #include_dirs=[np.get_include()],
                              extra_compile_args=extra_compile_args,
                              extra_link_args=extra_link_args
                              ),
                   ]
    
setup(
    name='pyPRISM',
    description='A python tool for Polymer Reference Interactions Site Model (PRISM) calculations',
    author='Tyler B. Martin',
    author_email = 'tyler.martin@nist.gov',
    url = 'https://github.com/usnistgov/pyprism',
    version=version,
    license='LICENSE',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
	classifiers = [
		'Development Status :: 4 - Beta',
		'Intended Audience :: Science/Research',
		'License :: Freely Distributable',
		'License :: Freeware',
		'License :: Public Domain',
		'Natural Language :: English',
		'Operating System :: MacOS',
		'Operating System :: Microsoft',
		'Operating System :: Unix',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 2 :: Only',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: Implementation :: CPython',
		'Topic :: Scientific/Engineering',
		'Topic :: Scientific/Engineering :: Chemistry',
		'Topic :: Scientific/Engineering :: Physics',
	],
	keywords = 'materials science polymer theory simulation X-ray neutron scattering liquid-state nanocomposite',
	project_urls = {
		'Bug Reports': 'https://github.com/usnistgov/pyprism/issues',
		'Source': 'https://github.com/usnistgov/pyprism',
		'Documentation': 'http://pyPRISM.readthedocs.io',
	},
    install_requires = ['numpy>=1.8.0','scipy','Cython','pint'],
    packages=find_packages(where='.'),
    package_data={'pyPRISM':['test/data/*dat','test/data/*csv']},
	ext_modules= ext_modules,
    cmdclass = cmdclass,
)

