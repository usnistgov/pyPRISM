#!python
'''
Adapted from https://github.com/scikit-image/skimage-tutorials/check_setup.py (ade46c2)

The goal of this file is to give users a clean and descriptive check of their environments.
'''
import sys
import os
from packaging.version import Version as LooseVersion

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    reqs = f.readlines()

#used for renaming packages
pkg_names = { }


for pkg_str in reqs:
    pkg_split = pkg_str.strip().split()
    if len(pkg_split)>1:
        pkg,eq,version = pkg_split
    else:
        pkg = pkg_split[0]
        version = '0.0.0'

    module_name = pkg_names.get(pkg, pkg)
    try:
        m = __import__(module_name)
        status = '✓'
    except ImportError as e:
        m = None
        if (pkg != 'numpy' and 'numpy' in str(e)):
            status = '?'
            version_installed = 'Needs NumPy'
        else:
            version_installed = 'Not installed'
            status = 'X'

    if m is not None:
        version_installed = m.__version__
        if LooseVersion(version) > LooseVersion(version_installed):
            status = 'X'

    if 'sphinx' in pkg:
        reqstring = '(only for building docs)'
    else:
        reqstring = ''

    print('[{}] {:<20} {:20} {}'.format(
        status, pkg.ljust(13), version_installed, reqstring)
        )
