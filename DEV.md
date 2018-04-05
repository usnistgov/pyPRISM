Distributing a Release
----------------------
1. Run unit-tests
```bash
$ pytest --verbose
```
2. Bump version in pyPRISM/version.py (see semver.org)
3. Update, compile, and check docs locally
```bash
$ cd docs
$ make clean html
```
4. Update CHANGES.md (git log)
5. Commit all updates to dev and push
```bash
$ git add -u
$ git commit
$ git push nistgit dev
```
6. Checkout master, merge dev, and push
```bash
$ git checkout master
$ git merge dev
$ git tag -a vX.X.X
$ git push nistgit master
$ git push nistgit master --tags
```
7. Create distributions
```
$ python setup.py build_ext
$ python setup.py sdist
```
8. Upload to pypi
    - twine upload --skip--existing dist/*
9.  Update conda-forge 
'''

Compiling C-Extentsions
-----------------------
python setup.py build_ext --inplace

