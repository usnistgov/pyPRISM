
Compiling C-Extentsions
-----------------------
python setup.py build_ext --inplace

Distributing a Release
----------------------
1. Run unit-tests
    - cd tests
    - python -m pytest --verbose
2. Bump version in pyPRISM/version.py
    - See semver.org
3. Update and compile docs locally
    - cd docs
    - make clean html
4. Update CHANGES.md
    - Use git log to survey changes
5. Commit all updates to dev and push
    - git commit
    - git push nistgit dev
6. Checkout master, merge dev, and push
    - git checkout master
    - git commit
    - git push nistgit master
    - git push nistgit master --tags
- Create distributions
    - python setup.py build_ext
    - python setup.py sdist
    - python setup.py bdist_wheel
- Upload to test.pypi.org
    - twine upload --repository-url https://test.pypi.org/legacy/ dist/*
- Upload to pypi.org
    - twine upload dist/*
- Update conda-forge 
'''
