# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    = -j 3
SPHINXBUILD   = python -msphinx
SPHINXPROJ    = pyPRISM
SOURCEDIR     = .
BUILDDIR      = _build

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
html: Makefile
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

buildapi:
	sphinx-apidoc -fMeT ../pyPRISM -o api
		@echo "Auto-generation of API documentation finished. " \
		"The generated files are in 'api/'"
	sed -i -e '/Submodules/,+1d' api/*
	sed -i -e '/Subpackages/,+2d' api/*
	sed -i -e 's/pyPRISM\ package/API/' api/pyPRISM.rst
	sed -i -e 's/\(\s*\)\(pyPRISM\.calculate\)/\1pyPRISM\.core\n\1\2/' api/pyPRISM.rst
	#sed -i -e 's/\.\. toctree::/\.\. toctree::\n\ \ \ \ :maxdepth: 1\n/g' api/pyPRISM.rst

clearapi:
	rm -rf api/*

allapi: clearapi buildapi

