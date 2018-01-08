Contributing
============

Thank you for taking the time to contribute! 

* [Asking for help](#asking-for-help)
* [Suggesting a feature](#suggesting-a-feature)
* [Filing a bug report](#filing-a-bug-report)
* [Submitting a pull request](#submitting-a-pull-request)

## Asking for help

Please use the [pyPRISM tutorial](https://github.com/usnistgov/pyPRISM_tutorial) 
before asking any questions. We have put a lot of effort into those notebooks
and many questions and techniques are answered there.

Please see the [faq](https://pyprism.readthedocs.io/en/latest/faq.html) and
[convergence tips](https://pyprism.readthedocs.io/en/latest/convergence.html)
pages of the documention documentation. Many questions are answered there.

If the above doesn't help, use the
[issues](https://github.com/usnistgov/pyPRISM/issues) interface to ask
questions! Please tag your question using the `question` tag. 

## Suggesting a feature

We can't think of everything. If you've got a good idea for a feature, then
please let us know.  If you require a feature urgently it's best to write it
yourself and share it with the community!

Use the [issues](https://github.com/usnistgov/pyPRISM/issues) interface to
suggest features! Please tag your suggestion with the `enhancement` tag.

When suggesting a feature, make sure to:

* Check the code on GitHub to make sure it's not already hiding in an unreleased version ;)
* Check existing issues, open and closed, to make sure it hasn't already been suggested

## Filing a bug report

If you run into a problem with one of our libraries or examples then please let
us know. Be as detailed as possible, and be ready to answer questions when we
get back to you.

Use the [issues](https://github.com/usnistgov/pyPRISM/issues) interface to
file bug reports! Please tag your suggestion with the `bug` tag.

Please include details such as:

* OS (Windows 8, Windows 10, OSX Sierra, Ubuntu 16.04)
* A *minimal* example that repoduces the behavior.
* Any solutions you've tried
* pyPRISM version
    ```python
        >>> from pyPRISM import Version 
        >>> print Version.version
    ```
* conda version
    ```bash
        $ conda --version
    ```

## Submitting a pull request

If you've decided to fix a bug or work on a feature it's best to let us know
what you're working on first. This can be done by filing an appropriate issue
as discussed above or commenting on an already assigned issue.

#### Do

* Do use PEP8 style guidelines
* Do use spaces not tabs in files 
* Do comment your code where necessary
* Do write basic unit-tests for all new classes/methods
* Do run the full test suite before submission
* Do follow the patterns set forth in other classes/methods
* Do write code for general use, not your specific use-case

#### Don't

* Don't make large changes to the core classes
* Don't add non-universal or trivial feature to the code
* Don't try to do too much at once

### Licensing

When you submit code to our libraries, you implicitly and irrevocably agree to
adopt the associated licenses. You should be able to find this in the file
named `LICENSE.`.

### Subitting your code

Once you're ready to share your contribution with us you should submit it as a
Pull Request. Fork pyPRISM onto your own GitHub, push your changes up to this
repo, and then file a Pull Request using the online interface. See
[here](https://help.github.com/articles/fork-a-repo/) for more details.

* Be ready to receive and embrace constructive feedback.
* Be prepared for rejection; we can't always accept contributions.
