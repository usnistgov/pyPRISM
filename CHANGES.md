# Changelog
See https://keepachangelog.com/en/1.0.0/

## [1.0.4] - 2020/07/01
### Added
- PRISM objects now store minimization object from scipy.root as PRISM.minimize_result
- Pair iterator utility to the core.System object

### Changed
- Many documentation fixes/tweaks
     
### Fixed
- FJC limit of omega.DiscreteKoyama was incorrect (thanks @Jadrich!)
- structure factor normalization flag was being ignored
- fixed domain check in omega.FromArray
- test suite for when test suite isn't available

## [1.0.3] - 2018/04/05
### Added
- MyBinder Support

## [1.0.2] - 2018/04/04
### Changed
- Moved tests back under pyPRISM

### Added 
- test() method to pyPRISM/__init__.py

## [1.0.1] - 2018/04/04
###Added
- Added LICENSE to MANIFEST.in
    - Yes, this required a version bump
    - See here: https://github.com/pypa/packaging-problems/issues/74

## [1.0.0] - 2018/04/01
### Added
- Initial Release! 

