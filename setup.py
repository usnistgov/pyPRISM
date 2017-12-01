from setuptools import setup,Extension,find_packages

import update_version

long,short = update_version.get_git_version()
version = short

setup(
    name='typyPRISM',
    description='A python tool for Polymer Reference Interactions Site Model (PRISM) calculations',
    author='Tyler B. Martin',
    author_email = 'tyler.martin@nist.gov',
    version=version,
    packages=find_packages(where='.'),
    license='LICENSE',
    long_description=open('README.md').read(),
)
